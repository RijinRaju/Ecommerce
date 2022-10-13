from datetime import date, datetime
from .models import sales_report,monthly_sales_report
from django.http import HttpResponse, response
from django.shortcuts import render,redirect
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.template import context
from django.views.decorators.cache import never_cache
from django.contrib import messages
from shop.models import Products,Category,Sub_category,Banners,Coupon,Category_offer,Product_offer
from customers.models import Customers
from orders.models import Order,OrderProduct
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator
from orders.forms import statusForm
from django.db.models import Count
from django.db.models.functions import ExtractDay,ExtractMonth
import sweetify
from django.utils import timezone
import xlwt
from  xhtml2pdf import pisa
from django.template.loader import get_template
import datetime
import csv
from django.views.decorators.cache import cache_control
from docx.shared import Inches

# Create your views here.


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login(request):
    if 'adminSession' in request.session:
        return redirect('admin_home')
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        admin = auth.authenticate(username=username, password=password,is_admin=True)
        print("admin",admin)
        if admin:
            auth.login(request, admin)
            request.session['adminSession'] = 'adminsession'
            user_data = Customers.objects.all()
            print(user_data)
            return redirect(home)
        else:
            messages.info(request, 'invalid credentials')
            return render(request, 'owner/login.html')
    else:
        return render(request, 'owner/login.html')

@login_required
def admin_logout(request,):
    if 'adminSession' in request.session:
        print(request.session.get('adminSession'))
        del request.session['adminSession']
        return redirect('admin_login')
    else:
        return redirect('admin_login')


@login_required(login_url='login')
def home(request):
    if 'adminSession' in request.session:
        orders = OrderProduct.objects.filter(ordered=True).annotate(Count('id'))
        sales = Order.objects.filter(status="Out of delivery").annotate(Count('id'))
        products = Products.objects.filter(is_available = True ).annotate(Count('id'))
        brand_orders = OrderProduct.objects.filter(ordered=True)
        customers = Customers.objects.all().count()

        days = Order.objects.annotate(day=ExtractDay('created_at')).values('day').annotate(count=Count('id')).values('day','count')

        total_orders = 0
        total_sales = 0
        total_products = 0


        day_date = []
        date_counter = []
        brand_name = []
        brand_order_count = []

        for brand in brand_orders:
            if brand.product.category.title not in brand_name:
                brand_name.append(brand.product.category.title)
                sum_prod = OrderProduct.objects.filter(product=brand.product.id).count()
                brand_order_count.append(sum_prod)
           
        for day in days:
            if day not in day_date:
                day_date.append(day['day'])
                date_counter.append(day['count'])

        for total_sale in sales:
            total_sales += total_sale.order_total

        for total_order in orders:
            total_orders += total_order.id__count

        for total_product in products:
            total_products += total_product.quantity


        context = {
            'total_sales':total_sales,
            'total_orders':total_orders,
            'total_products':total_products,
            'brand_name':brand_name,
            'brand_order_count':brand_order_count,
            'total_customers':customers,
            'day_date':day_date,
            'date_count':date_counter
        }
        return render(request, 'owner/home.html',context)
    else:
        return redirect('admin_login')



@login_required(login_url='login')
def products(request):
    if 'adminSession' in request.session:
        product_data=Products.objects.all()
        paginator = Paginator(product_data, 4)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)
        return render(request, 'owner/product.html',{'products_data':page_object})
    else:
        return render(request, 'owner/login.html' )

@login_required(login_url='login')
def add_product(request):
    if 'adminSession' in request.session:
        cat_data = Category.objects.all()
        product = Products.objects.all()
        print("catdat:",cat_data)
        if request.method == 'POST':
            pro = Products()
            pro.productName = request.POST.get('name')
            pro.price = request.POST.get('price')
            pro.discount_price = request.POST.get('price')
            pro.thumbnail = request.POST.get('thumbnail')
            category_id = request.POST.get('category')
            category = Category.objects.get(id = category_id)
            pro.category = category
            pro.quantity = request.POST.get('stocks')
            pro.descriptions = request.POST.get('desc')
            if len(request.FILES) != 0:
                pro.image1 = request.FILES['img1']
                pro.image2 = request.FILES['img2']
                pro.image3 = request.FILES['img3']
            pro.save()
            return redirect(products)
            # return render(request, 'owner/product.html', {"cat_data": cat_data,'products_data':product})
        else:
            return render(request, 'owner/add_products.html',{"cat_data":cat_data})
    return render(request, 'owner/add_products.html', {"pro_data": product})


@login_required(login_url='login')
def edit_product(request,id):
    if 'adminSession' in request.session:
        products=Products.objects.get(id=id)
        category=Category.objects.all()
        if request.method == 'POST':
            products.productName=request.POST['name']
            products.price=request.POST['price']
            products.discount_price = request.POST['price']
            products.quantity=request.POST['stocks']
            products.thumbnail=request.POST['thumbnail']
            products.description=request.POST['desc']
            category=request.POST['category'] #to pass values into a foreign key field take the object and assign to it
            cat= Category.objects.get(id=category)
            products.category = cat
            if len(request.FILES) != 0:
                products.image1 = request.FILES['img1']
                products.image2 = request.FILES['img1']
                products.image3 = request.FILES['img1']
            products.save()
            return redirect('products')
        return render(request,'owner/edit_products.html',{'products_data':products,'category':category})
    else:
        return render(request,'owner/login.html')

@login_required(login_url='login')
def delete_product(request,id):
    if 'adminSession' in request.session:
        del_data=Products.objects.get(id=id)
        del_data.delete()
        return  redirect(products)

@login_required(login_url='login')
def users(request):
    if 'adminSession' in request.session:
        customers=Customers.objects.all().filter(is_admin=False)
        paginator = Paginator(customers,5)
        page_number = request.GET.get("page")
        page_object = paginator.get_page(page_number)
        return render(request,'owner/users.html',{'customers':page_object})

@login_required(login_url='login')
def block_user(request,id):
    if 'adminSession' in request.session:
        blk_data=Customers.objects.get(id=id)
        if blk_data.status =="ACTIVE":
            blk_data.status ="BLOCK"
            blk_data.save()
            print("status1:",blk_data.status)
            return redirect('users')
        elif blk_data.status == "BLOCK":
            blk_data.status="ACTIVE"
            blk_data.save()
            print("status2:",blk_data.status)
            return redirect('users')
    customers = Customers.objects.all()
    return render(request,'owner/users.html',{'customers':customers})

@login_required(login_url='login')
def orders(request):
    order = OrderProduct.objects.filter(ordered = True)
    paginator = Paginator(order,4)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return render(request, 'owner/orders.html',{'order':page_object})

@login_required(login_url='login')
def order_details(request,id):
    order = OrderProduct.objects.get(id=id)
    ord = order.order_id
    orders = Order.objects.get(id = ord) #order id of individual items
    if request.method =="POST":
        orders.status = request.POST['status']
        orders.save()
        return render(request, 'owner/orders_details.html', {'order': order})
    else:
        return render(request,'owner/orders_details.html',{'order':order})




# category management..............................

class CategoryList(ListView):
    model = Category
    template_name = 'owner/category.html'



    # class CategoryCreate(CreateView):
    #     model = Category
    #     fields = "__all__"
    #     template_name = 'owner/add_category.html'

class CategoryUpdate(UpdateView):
    model = Category
    fields = "__all__"
    template_name = 'owner/category_update.html'




@login_required(login_url='login')
def subCategoryList(request):
    sub_cat_data=Sub_category.objects.all()
    return render(request,'owner/sub_category.html',{"sub_cat_data":sub_cat_data})




class SubCategoryCreate(CreateView):
    model = Sub_category
    fields = "__all__"
    template_name = 'owner/sub_add_category.html'

class SubCategoryUpdate(UpdateView):
    model = Sub_category
    fields = "__all__"
    template_name = 'owner/sub_category_update.html'



class Category_delete(DeleteView):
    model = Category
    template_name = 'owner/category_delete.html'


    def get_success_url(self):
        return reverse('category')

class Subcategory_delete(DeleteView):
    model = Sub_category
    template_name = 'owner/sub_category_delete.html'


    def get_success_url(self):
        return reverse('sub_category')


@login_required(login_url='login')
def add_category(request):
    if 'adminSession' in request.session:
        if request.method == 'POST':
            cate = Category()
            title = request.POST.get('title')
            url_slug = request.POST.get('url_slug')
            description = request.POST.get('desc')
            if len(request.FILES) != 0:
                thumbnail = request.FILES['thumbnail']
            if Category.objects.filter(title__icontains =title).exists():
                print("true category")
                messages.info(request,"category already exists")
            else:
                cate.title = title
                cate.url_slug = url_slug
                cate.description = description
                cate.thumbnail = thumbnail
                cate.save()
                return redirect('category')
                
    return render(request,'owner/add_category.html')



# Offer  management........................

@login_required(login_url='login')
def coupons(request):
    coupon = Coupon.objects.all().order_by('id')
    cat_offer = Category.objects.all()
    category_offer = Category_offer.objects.all()
    product_offer = Product_offer.objects.all()
    products_list = Products.objects.all()

    for ex_cp in coupon:
        
        if ex_cp.valid_until <= timezone.now():
            ex_cp.is_Active = False
            ex_cp.save()
            sweetify.success(request,"order is deleted")
    
    for ex_date in category_offer:
        product = Products.objects.filter(category=ex_date.category.id)
        if ex_date.valid_until <= date.today():
            ex_date.is_Active = False
            ex_date.save()
            for prod in product:
                prod.discount_price += int(ex_date.offer_amount)
                print("adding discount amounnt",prod.discount_price)
                prod.save()

    # comparing both product and category offers
    
  

    context={
        'coupon':coupon,
        'category':cat_offer,
        'category_offer': category_offer,
        'products_list':products_list,
        'product_offer':product_offer
    }
    return render(request, 'owner/coupons.html',context)



def add_coupon(request):
    coupon = Coupon()
    if request.method == "POST":
        coupon.title = request.POST['title']
        coupon.coupon_code = request.POST['code']
        coupon.valid_until = request.POST['valid_date']
        coupon.maximum_discount_amount = request.POST['amount']
        coupon.max_limit = request.POST['limit']
    coupon.save()
    context = {
        'coupon': coupon,
    }
    return redirect(coupons)



def add_category_offer(request):
    cate_offer = Category_offer()
    if request.method == "POST":
        cate_offer.offer_name = request.POST['offer_name']
        cate_offer.valid_until = request.POST['valid_date']
        value = request.POST['amount']
        cate_offer.offer_percent = value
        cat_id = request.POST['category']
        category = Category.objects.get(id=cat_id)
        cate_offer.category= category
        
    cate_offer.save()
    # try:
    #     category_offer_all = Category_offer.objects.all()
    #     for cat_off in category_offer_all:
    #         sel_cat = Products.objects.filter(category=cat_off.category)
    #         for cat in sel_cat:
    #             amt1 = int(cat_off.offer_percent)/100
    #             amt2 = amt1 * cat.discount_price
    #             print("product offers amount", amt2)
    #             prod = Product_offer.objects.filter(product=cat.id)
    #             for pro in prod:
    #                 if pro:
    #                     if pro.offer_amount > amt2:
    #                         cat.discount_price -= int(pro.offer_amount)
    #                         cat.save()
    #                     else:
    #                         cat.discount_price -= amt2
    #                         cat.save()
    # except:
    #     pass
    
    return redirect(coupons)


def delete_category_offer(request, id):
    if 'adminSession' in request.session:
        cat_offer = Category_offer.objects.get(id=id)
        cat_offer.delete()
        return redirect(coupons)
    else:
        return render(request, 'owner/login.html')



def edit_category_offer(request, id):
    category_offer = Category_offer.objects.get(id=id)
    category = Category.objects.all()
    if 'adminSession' in request.session:
        if request.method == "POST":
            category_offer.offer_name = request.POST['offer_name']
            category_offer.valid_until = request.POST['valid_date']
            value = request.POST['amount']
            category_offer.offer_percent = value
            cat_id = request.POST['category']
            category = Category.objects.get(id=cat_id)
            category_offer.category = category
            category_offer.save()
            return redirect(coupons)
        context = {
            'category_offer': category_offer,
            'category':category,
        }
        return render(request, 'owner/edit_category_offer.html', context)
    else:
        return render(request, 'owner/login.html')



def edit_coupon(request,id):
    coupon = Coupon.objects.get(id=id)
    if 'adminSession' in request.session:
        if request.method == "POST":
            coupon.title = request.POST['title']
            coupon.coupon_code = request.POST['code']
            coupon.valid_until = request.POST['valid_date']
            coupon.maximum_discount_amount = request.POST['amount']
            coupon.max_limit = request.POST['limit']
            coupon.save()
            return redirect(coupons)
        context={
            'coupon':coupon
        }
        return render(request, 'owner/edit_coupon.html',context)
    else:
        return render(request, 'owner/login.html')   


def delete_coupon(request,id):
    if 'adminSession' in request.session:
        coupon = Coupon.objects.get(id=id)
        coupon.delete()
        return redirect(coupons)
    else:
        return render(request,'owner/login.html')


# product offer management...............
def add_product_offer(request):
    category_offer = Category_offer.objects.all()
    product_offer = Product_offer()
    if request.method == "POST":
        percent = request.POST["percent"]
        product_id = request.POST['product']
        product = Products.objects.get(id=product_id)
        amt1 = int(percent)/100
        amt2 = amt1 * product.discount_price 
        product_offer.offer_amount = amt2
        product_offer.offer_percent = percent
        product_offer.product = product
        product_offer.save() 
      
    return redirect(coupons)


def edit_product_offer(request,id):
    product = Product_offer.objects.get(id=id)
    main_product = Products.objects.all()
    if request.method  == "POST":
        percent = request.POST["percent"]
        product_id = request.POST['product']
        prod = Products.objects.get(id=product_id)
        amt1 = int(percent)/100
        amt2 = amt1 * prod.discount_price
        product.offer_amount = amt2
        product.offer_percent = percent
        product.product = prod
        product.save()
        return redirect(coupons)
    context = {
        'product':product,
        'main_products':main_product
    }
    return render(request, 'owner/edit_product_offer.html', context)


def delete_product_offer(request,id):
    if 'adminSession' in request.session:
        product = Product_offer.objects.get(id=id)
        product.delete()
        return redirect(coupons)
    else:
        return render(request, 'owner/login.html')

# Banner management system................


@login_required(login_url='login')
def banner(request):
    if 'adminSession' in request.session:
        banner = Banners.objects.all()
        return render(request,'owner/banner.html',{'banner_data':banner})
    else:
        return render(request,'owner/login.html')

@login_required(login_url='login')
def add_banner(request):
    if 'adminSession' in request.session:
        if request.method == "POST":
            name = request.POST['banner_name']
            title = request.POST['banner_title']
            image = request.FILES['banner_img']
            banner = Banners.objects.create(title=title,name=name,banner=image)
            banner.save()
            return redirect('banner')
        return render(request,'owner/add_banners.html')
    else:
        return render(request,'owner/login.html')


@login_required(login_url='login')
def update_banner(request,id):
    if 'adminSession' in request.session:
        banner =Banners.objects.get(id=id)
        if request.method == "POST":
            banner.name = request.POST['banner_name']
            banner.title = request.POST['banner_title']
            if len(request.FILES) != 0:
                banner.banner = request.FILES['banner_img']
            banner.save()
            return redirect('banner')
        return render(request, 'owner/update_banner.html', {'banner_data': banner})
    else:
        return render(request,'owner/login.html')


@login_required(login_url='login')
def delete_banner(request,id):
    if 'adminSession' in request.session:
        del_data=Banners.objects.get(id=id)
        del_data.delete()
        return  redirect('banner')

# sales per day................
def sales(request):
    if 'adminSession' in request.session:
        if request.method == "GET":
            date = request.GET.get('date')
            
            Total = 0
            if date:
                excel_products = sales_report.objects.all().delete()
                products =OrderProduct.objects.order_by('-created_at').filter(created_at__icontains=date)
                
                for product in products:
                    excel_products = sales_report()
                    excel_products.date = product.created_at
                    excel_products.product_name = product.product.productName
                    excel_products.quantity = product.quantity
                    excel_products.amount = product.order.order_total
                    Total += product.order.order_total
                    excel_products.save()
                paginator = Paginator(products,20)
                page_number = request.GET.get('page')
                products_page = paginator.get_page(page_number)
                context = {
                'products':products_page,
                'Total':Total
                }
                return render(request,'owner/sales.html',context)
        
        Total = 0
        products = OrderProduct.objects.all().order_by('-created_at')
        for product in products:
            excel_products = sales_report()
            excel_products.date = product.created_at
            excel_products.product_name = product.product.productName
            excel_products.quantity = product.quantity
            excel_products.amount = product.order.order_total
            Total += product.order.order_total
            excel_products.save()
        paginator = Paginator(products,20)
        page_number = request.GET.get('page')
        products_page = paginator.get_page(page_number)
        context = {
                'products': products_page,
                'Total': Total
        }
        return render(request, 'owner/sales.html', context)

    return render(request,'owner/sales.html')

# sales per month.............................
def monthly_sales(request):
    if 'adminSession' in request.session:
        if request.method == "POST":
            month_date = request.POST['month_date']
            print("monthly ",month_date)
            Total = 0
            if month_date:
                excel_products = sales_report.objects.all().delete()
                # months = OrderProduct.objects.annotate(month=ExtractMonth('created_at'))
                months = OrderProduct.objects.filter(created_at__icontains = month_date )
                print("months",months)
                for month in months:
                    excel_products = sales_report()
                    excel_products.date = month.created_at
                    excel_products.product_name = month.product.productName
                    excel_products.quantity = month.quantity
                    excel_products.amount = month.order.order_total
                    Total += month.order.order_total
                    excel_products.save()
                paginator = Paginator(months,20)
                page_number = request.GET.get('page')
                months_page = paginator.get_page(page_number)
                context = {
                    'products': months_page,
                    'Total':Total
                }
                return render(request, 'owner/sales.html', context)

    return redirect(sales)



def yearly_sales(request):
    if 'adminSession' in request.session:
        if request.method == "POST":
            year_month_date = str(request.POST['year_date'])
            year_date = year_month_date[0:4]
            Total = 0
            if year_date:
                excel_products = sales_report.objects.all().delete()
                # months = OrderProduct.objects.annotate(month=ExtractMonth('created_at'))
                months = OrderProduct.objects.filter(created_at__icontains = year_date)
                for month in months:
                    excel_products = sales_report()
                    excel_products.date = month.created_at
                    excel_products.product_name = month.product.productName
                    excel_products.quantity = month.quantity
                    excel_products.amount = month.order.order_total
                    Total += month.order.order_total
                    excel_products.save()
                paginator = Paginator(months,20)
                page_number = request.GET.get('page')
                months_page = paginator.get_page(page_number)
                context = {
                    'products': months_page,
                    'Total':Total
                }
                return render(request, 'owner/sales.html', context)

    return redirect(sales)




# sales per day excel and pdf download................
@login_required(login_url='login')
def export_to_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['content-Disposition'] = 'attachment; filename="sales.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    # this will generate a file named as sales Report
    ws = wb.add_sheet('Sales Report')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Date','Product Name', 'Quantity', 'Amount', ]

    for col_num in range(len(columns)):
    # at 0 row 0 column
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    total = 0
    rows = sales_report.objects.all().values_list('date','product_name', 'quantity', 'amount')

    print("row", rows)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def export_to_pdf(request):
    total_sales = 0
    report = sales_report.objects.all()
    sales = Order.objects.filter(status="Out of delivery").annotate(Count('id'))

    for total_sale in report:
        total_sales += total_sale.amount

    template_path = 'owner/sales_pdf.html'
    context = {
        'report':report,
        'total_amount':total_sales,
    }
    
    # csv file can also be generated using content_type='application/csv
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response


def export_to_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement; filename=SalesReport' +str(datetime.datetime.now())+'.csv'


    writer = csv.writer(response)
    writer.writerow(['Date ','Product Name ','Quantity  ','Amount'])

    reports = sales_report.objects.all()

    for report in reports:
        writer.writerow([report.date , report.product_name , report.quantity  , report.amount ])
    return response

# sales monthly excel and pdf download................
@login_required(login_url='login')
def monthly_export_to_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['content-Disposition'] = 'attachment; filename="sales.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    # this will generate a file named as sales Report
    ws = wb.add_sheet('Sales Report')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Date', 'Product Name', 'Quantity', 'Amount', ]

    for col_num in range(len(columns)):
        # at 0 row 0 column
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()
    total = 0
    rows = monthly_sales_report.objects.all().values_list(
        'date', 'product_name', 'quantity', 'amount')

    print("row", rows)
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


@login_required(login_url='login')
def monthly_export_to_pdf(request):
    total_sales = 0
    report = monthly_sales_report.objects.all()
    sales = Order.objects.filter(
        status="Out of delivery").annotate(Count('id'))

    for total_sale in report:
        total_sales += total_sale.amount

    template_path = 'owner/sales_pdf.html'
    context = {
        'report': report,
        'total_amount': total_sales,
    }

    # csv file can also be generated using content_type='application/csv
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response


@login_required(login_url='login')
def monthly_export_to_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachement; filename=SalesReport' +str(datetime.datetime.now())+'.csv'


    writer = csv.writer(response)
    writer.writerow(['Date ','Product Name ','Quantity  ','Amount'])

    reports = monthly_sales_report.objects.all()

    for report in reports:
        writer.writerow([report.date , report.product_name , report.quantity  , report.amount ])
    return response
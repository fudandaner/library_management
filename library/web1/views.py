from django.shortcuts import render, redirect
from web1 import models
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponseRedirect


# Create your views here.
def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    id = request.POST.get("id")
    psd = request.POST.get("psd")
    student = models.Students.objects.filter(StudentID=id, Password=psd).first()
    if student:
        return redirect("/library/" + str(id) + "/list/")
    return render(request, "login.html", {"student_not_found": True})


def manage_login(request):
    if request.method == "GET":
        return render(request, "manage_login.html")
    id = request.POST.get("id")
    psd = request.POST.get("psd")
    if id == "rqh2001" and psd == "1.tangtang":
        return redirect("/manage_library/list/")
    return render(request, "manage_login.html", {"count_not_found": True})


def register(request):
    if request.method == "GET":
        context = {
            "gender_choice": models.Students.gender_choices,
        }
        return render(request, "register.html", context)
    Name = request.POST.get("Name")
    Password = request.POST.get("Password")
    Gender = request.POST.get("Gender")
    Grade = request.POST.get("Grade")
    Major = request.POST.get("Major")

    models.Students.objects.create(Name=Name, Password=Password, Gender=Gender, Grade=Grade, Major=Major)
    new_id = models.Students.objects.filter(Name=Name, Password=Password, Gender=Gender, Grade=Grade,
                                            Major=Major).last().StudentID
    context1 = {
        "has_created": True,
        "new_id": new_id
    }
    return render(request, "register.html", context1)


def library_list(request, id):
    queryset = models.Books.objects.all()
    queryset_count = queryset.count()
    context = {
        "queryset": queryset,
        "id": int(id),
        "queryset_count":queryset_count
    }
    return render(request, "library_list.html", context)


def manage_library_list(request):
    queryset = models.Books.objects.all()
    context = {
        "queryset": queryset,
    }
    return render(request, "manage_library_list.html", context)


def book_add(request):
    if request.method == "GET":
        return render(request, "book_add.html")

    Title = request.POST.get("Title")
    Author = request.POST.get("Author")
    Publisher = request.POST.get("Publisher")
    PublishDate = request.POST.get("PublishDate")
    ISBN = request.POST.get("ISBN")
    Price = request.POST.get("Price")
    book = models.Books.objects.filter(ISBN=ISBN).first()

    if book:
        # 更新现有书籍的库存数量
        a = book.StockQty + 1
        models.Books.objects.filter(ISBN=ISBN).update(StockQty=a)
        models.Books.objects.create(
            Title=Title,
            Author=Author,
            Publisher=Publisher,
            PublishDate=PublishDate,
            ISBN=ISBN,
            Price=Price,
            StockQty=a
        )
    else:
        # 创建新的书籍记录
        models.Books.objects.create(
            Title=Title,
            Author=Author,
            Publisher=Publisher,
            PublishDate=PublishDate,
            ISBN=ISBN,
            Price=Price,
        )
    return redirect("/manage_library/list/")


def book_edit(request, nid):
    row = models.Books.objects.filter(BookID=nid).first()
    if request.method == 'GET':
        # 对象是列表要用first取
        return render(request, "book_edit.html", {"row": row})
    Title = request.POST.get("Title")
    Author = request.POST.get("Author")
    Publisher = request.POST.get("Publisher")
    PublishDate = request.POST.get("PublishDate")
    ISBN = request.POST.get("ISBN")
    Price = request.POST.get("Price")
    if row.ISBN == ISBN:
        models.Books.objects.filter(BookID=nid).update(
            Title=Title,
            Author=Author,
            Publisher=Publisher,
            PublishDate=PublishDate,
            ISBN=ISBN,
            Price=Price,
        )
    else:
        book = models.Books.objects.filter(ISBN=ISBN).first()
        if book:
            # 更新现有书籍的库存数量
            a = book.StockQty + 1
            models.Books.objects.filter(ISBN=ISBN).update(StockQty=a)
            models.Books.objects.filter(BookID=nid).update(
                Title=Title,
                Author=Author,
                Publisher=Publisher,
                PublishDate=PublishDate,
                ISBN=ISBN,
                Price=Price,
                StockQty=a
            )
        else:
            models.Books.objects.filter(BookID=nid).update(
                Title=Title,
                Author=Author,
                Publisher=Publisher,
                PublishDate=PublishDate,
                ISBN=ISBN,
                Price=Price,
                StockQty=1
            )
        orinign = models.Books.objects.filter(ISBN=row.ISBN).first()
        if orinign:
            a = orinign.StockQty
            models.Books.objects.filter(ISBN=row.ISBN).update(StockQty=a - 1)
    return redirect("/library/list/")


def book_delete(request):
    nid = request.GET.get("nid")
    a = models.Books.objects.filter(BookID=nid).first().StockQty
    ISBN = models.Books.objects.filter(BookID=nid).first().ISBN
    models.Books.objects.filter(ISBN=ISBN).all().update(StockQty=a - 1)
    models.Books.objects.filter(BookID=nid).delete()
    return redirect("/manage_library/list/")


def manage_book_search(request):
    if request.method == "GET":
        context = {
            "lend_choice": models.Books.lend_choices,
        }
        return render(request, "manage_book_search.html", context)
    Title = request.POST.get("Title")
    Author = request.POST.get("Author")
    Publisher = request.POST.get("Publisher")
    PublishDate = request.POST.get("PublishDate")
    ISBN = request.POST.get("ISBN")
    Price = request.POST.get("Price")
    LendState = request.POST.get("LendState")
    query = Q()
    if Title:
        query &= Q(Title=Title)
    if Author:
        query &= Q(Author=Author)
    if Publisher:
        query &= Q(Publisher=Publisher)
    if PublishDate:
        query &= Q(PublishDate=PublishDate)
    if ISBN:
        query &= Q(ISBN=ISBN)
    if Price:
        query &= Q(Price=Price)
    if LendState:
        query &= Q(LendState=LendState)

    queryset = models.Books.objects.filter(query)
    queryset_count = queryset.count()
    context = {
        "queryset": queryset,
        "queryset_count": queryset_count
    }
    return render(request, "search_list.html", context)


def student_book_search(request, id):
    if request.method == "GET":
        context = {
            "lend_choice": models.Books.lend_choices,
            "id": id
        }
        return render(request, "student_book_search.html", context)
    Title = request.POST.get("Title")
    Author = request.POST.get("Author")
    Publisher = request.POST.get("Publisher")
    PublishDate = request.POST.get("PublishDate")
    ISBN = request.POST.get("ISBN")
    Price = request.POST.get("Price")
    query = Q()
    if Title:
        query &= Q(Title=Title)
    if Author:
        query &= Q(Author=Author)
    if Publisher:
        query &= Q(Publisher=Publisher)
    if PublishDate:
        query &= Q(PublishDate=PublishDate)
    if ISBN:
        query &= Q(ISBN=ISBN)
    if Price:
        query &= Q(Price=Price)

    queryset = models.Books.objects.filter(query)
    queryset_count = queryset.count()
    context = {
        "queryset": queryset,
        "queryset_count": queryset_count,
        "id": id
    }
    return render(request, "student_search_list.html", context)


def student_rent(request, nid, id):
    today = timezone.now().date()
    models.BorrowRecords.objects.create(BookID_id=nid, StudentID_id=id, BorrowDate=today)
    book = models.Books.objects.filter(BookID=nid).first()
    a = book.StockQty - 1
    ISBN = models.Books.objects.filter(BookID=nid).first().ISBN
    models.Books.objects.filter(ISBN=ISBN).update(StockQty=a)
    models.Books.objects.filter(BookID=nid).update(LendState=2)
    return render(request, "student_search_list.html", {"borrow_success": True, "id": id})


def student_rent_record(request, id):
    qst = models.BorrowRecords.objects.filter(StudentID_id=id).all()
    queryset_count = qst.count()
    return render(request, "student_rent_record_list.html", {"qst": qst, "id": id,"queryset_count":queryset_count})


def manage_rent_record(request):
    if request.method == "GET":
        return render(request, "manage_rent_search.html")
    book_id = request.POST.get("book_id")
    student_id = request.POST.get("student_id")
    LendState = request.POST.get("LendState")
    query = Q()
    if book_id:
        query &= Q(BookID=book_id)
    if student_id:
        query &= Q(StudentID=student_id)
    if LendState == "3":
        qst = models.BorrowRecords.objects.select_related('BookID').filter(query).all()
        queryset_count=qst.count()
        return render(request, "manage_rent_record_list.html", {"qst": qst,"queryset_count":queryset_count})
    if LendState == "1":
        query &= Q(ReturnDate__isnull=True)
        qst = models.BorrowRecords.objects.select_related('BookID').filter(query).all()
        queryset_count = qst.count()
        return render(request, "manage_rent_record_list.html", {"qst": qst,"queryset_count":queryset_count})
    if LendState == "2":
        query &= Q(ReturnDate__isnull=False)
        qst = models.BorrowRecords.objects.select_related('BookID').filter(query).all()
        queryset_count = qst.count()
        return render(request, "manage_rent_record_list.html", {"qst": qst,"queryset_count":queryset_count})

def manage_student_record(request):
    queryset = models.Students.objects.all()
    queryset_count = queryset.count()
    context = {
        "queryset": queryset,
        "queryset_count":queryset_count
    }
    return render(request, "manage_student_record.html", context)

def student_return(request, Borrowid, id):
    today = timezone.now().date()
    models.BorrowRecords.objects.filter(BorrowID=Borrowid).update(ReturnDate=today)
    nid = models.BorrowRecords.objects.filter(BorrowID=Borrowid).first().BookID_id
    book = models.Books.objects.filter(BookID=nid).first()
    a = book.StockQty + 1
    ISBN = models.Books.objects.filter(BookID=nid).first().ISBN
    models.Books.objects.filter(ISBN=ISBN).update(StockQty=a)
    models.Books.objects.filter(BookID=nid).update(LendState=1)
    return render(request, "student_rent_record_list.html", {"return_success": True, "id": id})


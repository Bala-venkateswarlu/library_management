from django.shortcuts import render, redirect
from django.http import HttpResponse
from library_management.models import Library
from library_management.models import Books
from library_management.models import Reader
# Create your views here.


# to navigate all pages 
def home(request):
    user_id = request.session.get('email')
    request.session['email1'] = user_id 
    print(user_id)
    if not user_id:
        return redirect('login')  # Redirect to login if not logged in
    return render(request, 'library_management/home.html')



def books(request):
    #books = Books.objects.all()
    search_query = request.GET.get('query','')  # Get the search query from the GET request
    #print(search_query)

    if search_query:
        # Filter books by the search query (case-insensitive search on the book name)
        books = Books.objects.filter(book_name__icontains=search_query)
    else:
        # If no search query, display all books
        books = Books.objects.all()
    return render(request, 'library_management/books.html',{'books':books}) #for displaying the books from database
    #return render(request, 'library_management/books.html')

def bag(request):
    if request.method == 'POST':
        print('post')
        reader_name = request.POST.get('reader_name')
        reference_id = request.POST.get('email')
        book_id = request.POST.get('book_id')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        # Get the selected book from the Books model
        try:
            book = Books.objects.get(id=book_id)
        except Books.DoesNotExist:
            return HttpResponse("Book does not exist.")

        # Save book details and reader details to the Reader model
        reader = Reader(
                        reader_name=reader_name,
                        reference_id=reference_id,
                        book_name=book.book_name,
                        Author=book.Author,  # Save Author
                        published=book.published,  # Save Published Date
                        start_date=start_date, 
                        end_date=end_date
                        )
        reader.save()

        # Remove the book from the Books model after borrowing
        book.delete()
        #return HttpResponse('go back')
        return redirect('books')  # Redirect back to the books list after borrowing

    # For GET request, display available books
    '''books = Books.objects.all()
    print('get')
    return render(request, 'library_management/bag.html', {'books': books} )'''

def pre_bag(request):
    books = Books.objects.all()
    return render(request, 'library_management/bag.html', {'books': books} )


def returns(request):
    
    if request.method == 'POST':
        # Get the reader_id from the POST request (when the user clicks "Return" button)
        reader_id = request.POST.get('reader_id')
       

        try:
            # Fetch the borrowed book record from the Reader model
            borrowed_book = Reader.objects.get(id=reader_id)
        except Reader.DoesNotExist:
            return HttpResponse("Record not found.")

         # Add the book back to the Books model with the original id, author, and published date
        returned_book, created = Books.objects.update_or_create(
            id=borrowed_book.id,  # Preserve the original ID
            defaults={
                'book_name': borrowed_book.book_name,
                'Author': borrowed_book.Author,  # Restore Author
                'published': borrowed_book.published  # Restore Published Date
            }
        )



        returned_book.save()

        # Remove the borrowed book entry from the Reader model
        borrowed_book.delete()

        return redirect('returns')  # Redirect back to the returns page
    
    # If the request is a GET, handle the case by displaying the list of borrowed books.
    elif request.method == 'GET':
        # Assuming you want to redirect to 'pre_returns' in case of a GET request
        return redirect('pre_returns')

    # Fallback in case of an unsupported HTTP method
    return HttpResponse("Method not allowed", status=405)

    # If request is GET, display the list of borrowed books
    #print("gets")
    #readers = Reader.objects.all()
   # return render(request, 'library_management/returns.html', {'readers': readers})
    #return render(request, 'library_management/returns.html')

def pre_returns(request):
    user_id = request.session.get('email')
    request.session['email2'] = user_id 
    readers = Reader.objects.filter(reference_id =user_id ) # display the list of borrowed books
    return render(request, 'library_management/returns.html', {'readers': readers})

#for saving  a new user registration in database
def reader(request):
    users = Library.objects.all()


    

    if request.method == 'POST':
        # Get data from the POST request
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        reference_id = request.POST.get('reference_id')
        email = request.POST.get('email')
        adress = request.POST.get('adress')

         # Debugging: Print received data
        print(f"Received POST data: {name}, {contact}, {reference_id}, {email}, {adress}")

        if not name or not contact or not reference_id or not email or not adress:
            return HttpResponse("All fields are required")
        
        # Check if the user already exists
        if Library.objects.filter(email=email).exists():
            return HttpResponse("Email already registered")
        
        new_user = Library(name=name, contact=contact, reference_id=reference_id,email=email,adress=adress)

        new_user.save()

        return HttpResponse("User registered successfully!")
    
        
    return render(request, 'library_management/readers.html', {'users':users})


def pre_readers(request):
    user_id = request.session.get('email1')
    users = Library.objects.filter(email=user_id)
    return render(request, 'library_management/readers.html', {'users':users})

       



# View to handle adding a new book
def add_book_view(request):
    if request.method == 'POST':
        print('post')
        # Get form data
        book_name = request.POST.get('book_name')
        author = request.POST.get('author')
        published = request.POST.get('published')

        # Save new book to the database
        new_book = Books(book_name=book_name, Author=author, published=published)
        new_book.save()

        # Redirect back to the book list page after saving
        return redirect('books')  # Redirect to the main books page
    print('get')
    # Render the form template if not a POST request
    return render(request, 'library_management/add_book.html')










def register(request):
    if request.method == 'POST':
        # Get data from the POST request
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        reference_id = request.POST.get('reference_id')
        email = request.POST.get('email')
        address = request.POST.get('address')
        password = request.POST.get('password')

        # Debugging: Print received data
        #print(f"Received POST data: {name}, {contact}, {reference_id}, {email}, {address}, {password}")

        # Basic validation
        if not name or not contact or not reference_id or not email or not address or not password:
            return HttpResponse("All fields are required")

        # Check if the user already exists
        if Library.objects.filter(email=email).exists():
            return HttpResponse("Email already registered. Please log in.")

        # Create and save new user
        new_user = Library(name=name, contact=contact, reference_id=reference_id, email=email, adress=address, password=password)
        new_user.save()

        #return HttpResponse("User registered successfully!")
        return redirect('login')

    return render(request, 'library_management/register.html')  # Create a template for 


def login(request):
    if request.method == 'POST':
        print("post")
        email = request.POST.get('email')
        # You can also use username or reference_id if required
        password = request.POST.get('password')  

        # Fetch user details
        try:
            user = Library.objects.get(email=email, password=password)
            # You may want to validate the password here (if you add a password field)
            request.session['user_id'] = user.id  # Store user ID in session
            request.session['email'] = user.email

            return redirect('home')  # Redirect to user home after login
        except Library.DoesNotExist:
            return HttpResponse("Invalid email or password.")
        
    print("Get")

    #return render(request, 'library_management/login.html')  # Create a template for login

def pre_login(request):

    return render(request, 'library_management/login.html')




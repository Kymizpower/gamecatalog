from django.shortcuts import render, redirect
from .forms import ContactForm
from django.contrib import messages

def contacts(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сообщение отправлено!')
            return redirect('contacts')
    else:
        form = ContactForm()
    return render(request, 'contacts/contacts.html', {'form': form})
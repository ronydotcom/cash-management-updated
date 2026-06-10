from django.shortcuts import render,redirect
from django.shortcuts import render, redirect, get_object_or_404

from cash_management.models import*
from cash_management.forms import *

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.messages import get_messages

from django.db.models import Sum



## registration page ##


def register_page(request):
    if request.method=='POST':
        form_data = RegistrationForm(request.POST)
        if form_data.is_valid():
            form_data.save()
            messages.success(request,'registration complete')
            return redirect('login_page')
    else:
        form_data=RegistrationForm()
    context={
        'form_data' : form_data,
        'form_title' : 'Registration Form',
        'form_btn' : 'save'
    }
    return render(request,'master/base-form.html',context)




###login page####

def login_page(request):
    form_data = AuthenticationForm(request, data=request.POST)
    if request.method=='POST':
        if form_data.is_valid():
            user=form_data.get_user()
            login(request,user)
            return redirect('dashboard_page')
    context={
        'form_data' : form_data,
        'form_title' : "LOGIN FORM",
        'form_btn' : 'save'
    }
    return render(request,'master/base-form.html',context)




###logout page###


@login_required
def logout_page(request):
    logout(request)
    messages.success(request,'logout success')
    return redirect('login_page')




### profile create edit delete page ###


@login_required
def profile_page(request):
    profile=InfoModel.objects.filter(
        user=request.user).first()
    if request.method=='POST':
        form_data = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile)
        
        if form_data.is_valid():
            save_data = form_data.save(commit=False)
            save_data.user=request.user
            save_data.gender = save_data.gender
            save_data.age = save_data.age 
            
            save_data.save()
            if profile:
                messages.success(request,
                'Profile updated successfully')
            else:
                messages.success(request,
                'Profile Created Successfully')
            return redirect('profile_page')
    
    if request.method=='POST' and 'delete_profile' in request.POST:
        if profile:
            profile.delete()
            messages.success(request,'Profile Deleted Successfully')
        return redirect('profile_page')

    else:
        form_data = ProfileForm(instance=profile)

    if not profile or request.GET.get('edit'):
        context={
        'form_data' : form_data,
        'form-title' : 'profile form',
        'form_btn' : 'Save profile'
    }
        return render(request,'master/base-form.html', context)

    return render(request,'profile.html',{'profile' : profile})




@login_required
def dashboard_page(request):
    cash_data = AddCash.objects.filter(user = request.user).order_by('-id')
    expense_data = Expense.objects.filter(user=request.user).order_by('-id')

    total_cash = cash_data.aggregate(total=Sum('amount')) ['total'] or 0
    total_expense = expense_data.aggregate(total=Sum('amount')) ['total'] or 0

    balance = total_cash - total_expense

    context={
        'total_cash' : total_cash,
        'total_expense' : total_expense,
        'balance' : balance,
        'cash_data' : cash_data,
        'expense_data' : expense_data,
    }

    return render(request,'dashboard.html',context)


@login_required

def cash_page(request):
    cash_data = AddCash.objects.filter(user = request.user).order_by('-id')
    context ={
        'cash_data' : cash_data
    }
    return render(request,'cash.html',context)


@login_required
def addcash_page(request):
    if request.method == 'POST':
        form_data = AddCashForm(request.POST)
        if form_data.is_valid():
            cash = form_data.save(commit=False)
            cash.user = request.user
            cash.save()
            messages.success(request,'Cash Added Successfully')
            return redirect(cash_page)
    else:
        form_data = AddCashForm()
    context = {
        'form_data' : form_data,
        'form_title' : 'Ádd Cash',
        'form_btn' : 'Add Cash',
    }
    return render(request,'master/base-form.html',context)



@login_required
def update_cash_page(request, id):

    cash = get_object_or_404(AddCash,id=id,user=request.user)

    if request.method == 'POST':

        form_data = AddCashForm(request.POST,instance=cash)

        if form_data.is_valid():

            form_data.save()

            messages.success(request,'Cash Updated Successfully')
            return redirect('cash_page')
    else:

        form_data = AddCashForm(instance=cash)

    context = {
        'form_data': form_data,
        'form_title': 'Update Cash',
        'form_btn': 'Update Cash',
    }

    return render(request,'master/base-form.html',context)





@login_required
def delete_cash_page(request, id):

    cash = get_object_or_404(
        AddCash,
        id=id,
        user=request.user
    )

    cash.delete()

    messages.success(
        request,
        'Cash Deleted Successfully'
    )

    return redirect('cash_page')








@login_required
def expense_page(request):
    expense_data = Expense.objects.filter(user=request.user).order_by('-id')
    context = {
        'expense_data': expense_data
    }
    return render(request, 'expense.html', context)




@login_required
def addexpense_page(request):
    if request.method == 'POST':
        form_data = ExpenseForm(request.POST)
        if form_data.is_valid():
            cash = form_data.save(commit=False)
            cash.user = request.user
            cash.save()
            messages.success(request,'Expenses Added Successfully')
            return redirect(expense_page)
    else:
        form_data = ExpenseForm()
    context = {
        'form_data' : form_data,
        'form_title' : 'Ádd expenses',
        'form_btn' : 'Add expenses',
    }
    return render(request,'master/base-form.html',context)



@login_required
def update_expense_page(request,id):
    expense = get_object_or_404(Expense,id=id,user=request.user)

    if request.method == 'POST':
        form_data = ExpenseForm(request.POST,instance=expense)

        if form_data.is_valid():
            form_data.save()
            messages.success(request,'Expense Updated Successfully')
            return redirect('expense_page')
    else:
        form_data = ExpenseForm(instance=expense)

    return render(request,'master/base-form.html',{
        'form_data': form_data,
        'form_title': 'Update Expense',
        'form_btn': 'Update Expense',
    })


@login_required
def delete_expense_page(request,id):
    expense = get_object_or_404(Expense,id=id,user=request.user)
    expense.delete()
    messages.success(request,'Expense Deleted Successfully')
    return redirect('expense_page')





""" aggregate(total=Sum('amount')) means: "Calculate sum of 
amount and store result using name total". here Django 
returns:

{
    'total': 500
}

Then:

['total']

gets only: 500
"""
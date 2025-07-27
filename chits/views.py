from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Member, PaymentHistory
from datetime import date, datetime
from django.db.models import Q

MOM_PASSWORD = "Akash@123"  # Change this to whatever you like


# 🛡️ Mom Authentication
def require_mom_auth(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('mom_authenticated'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper


# 🏠 Home Page
def home(request):
    members_10k = Member.objects.filter(plan='10000')
    members_20k = Member.objects.filter(plan='20000')
    return render(request, 'home.html', {
        'members_10k': members_10k,
        'members_20k': members_20k
    })

def public_plan_table(request, plan_amount):
    if plan_amount not in ['10000', '20000']:
        return HttpResponse("Invalid Plan", status=400)
    members = Member.objects.filter(plan=plan_amount)
    return render(request, 'plan_table.html', {
        'members': members,
        'plan': plan_amount
    })




def plan_table(request, amount):
    if amount not in [10000, 20000] and not request.session.get("mom_authenticated"):
        return redirect('mom_login')

    members = Member.objects.filter(plan=amount)
    return render(request, 'plan_table.html', {
        'amount': amount,
        'members': members
    })



# 🔐 Login
def mom_login(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        if password == MOM_PASSWORD:
            request.session['mom_authenticated'] = True
            return redirect('view_members')
        else:
            return render(request, 'login.html', {'error': 'Invalid password'})
    return render(request, 'login.html')


# 🚪 Logout
def mom_logout(request):
    request.session.flush()
    return redirect('home')


# ➕ Add Member
@require_mom_auth
def add_member(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        plan = request.POST.get('plan')
        chitti_lifted = request.POST.get('chitti_lifted') == 'on'
        Member.objects.create(name=name, phone=phone, plan=plan, chitti_lifted=chitti_lifted)
        return redirect('view_members')
    return render(request, 'add_member.html')


# 👀 View Members
@require_mom_auth
def view_members(request, plan=None):
    if plan == '10000' or plan == '20000':
        members = Member.objects.filter(plan=plan)
    else:
        members = Member.objects.all()
    return render(request, 'view_members.html', {'members': members})

@require_mom_auth

def view_members_by_plan(request, plan):
    members = Member.objects.filter(group__plan_amount=plan).order_by('-created_at')
    return render(request, 'view_members_by_plan.html', {'members': members, 'plan': plan})

# ❌ Delete Member
@require_mom_auth
def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.delete()
    return redirect('view_members')


# 🧾 Member Detail
@require_mom_auth
def member_detail(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    return render(request, 'member_detail.html', {'member': member})


# 📅 Monthly Tracker
@require_mom_auth
def monthly_tracker(request):
    today = date.today()
    first_day_of_month = date(today.year, today.month, 1)

    # Ensure payment history exists for this month
    members = Member.objects.all()
    for member in members:
        PaymentHistory.objects.get_or_create(member=member, month=first_day_of_month)

    paid = PaymentHistory.objects.filter(month=first_day_of_month, is_paid=True)
    unpaid = PaymentHistory.objects.filter(month=first_day_of_month, is_paid=False)

    return render(request, 'monthly_tracker.html', {
        'paid': paid,
        'unpaid': unpaid,
        'month': first_day_of_month.strftime('%B %Y')
    })


# ✅ Mark Paid
@require_mom_auth
def mark_paid(request, history_id):
    history = get_object_or_404(PaymentHistory, id=history_id)
    history.is_paid = True
    history.save()
    return redirect('monthly_tracker')


# ❌ Mark Unpaid
@require_mom_auth
def mark_unpaid(request, history_id):
    history = get_object_or_404(PaymentHistory, id=history_id)
    history.is_paid = False
    history.save()
    return redirect('monthly_tracker')


from django.shortcuts import render
from django.http import HttpResponse

def plan_table(request, amount):
    rows = []

    if amount == 20000:
        total = 480000
        for i in range(1, 26):
            rows.append({'sno': i, 'amount': amount, 'total': total})
            total += 5000

    elif amount == 10000:
        total = 240000
        for i in range(1, 26):
            rows.append({'sno': i, 'amount': amount, 'total': total})
            total += 2500

    elif amount == 5000:
        total = 95000
        for i in range(1, 21):  # 20 months
            rows.append({'sno': i, 'amount': amount, 'total': total})
            total += 1000  # Increase by 1k each month

    else:
        return HttpResponse("Invalid plan amount", status=400)

    return render(request, 'plan_table.html', {'amount': amount, 'rows': rows})



from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
import json
import hashlib as hl

# main page function

def index(request):
    context = {}



    if not request.user.is_authenticated:
        return redirect("login")

    if request.user.is_superuser:
        if not invivation.objects.filter(invited_by=request.user).exists():
            new_invitation = invivation(
                invited_by = request.user,
                code = generate_code(request.user.username),
            )

            new_invitation.save()

        return redirect("adminPage")
    else:
        temp_ref = tree_data.objects.get(node=request.user)

        if temp_ref.is_out:
            context['info'] = balance.objects.get(which_user=request.user)
            context['is_out'] = True
            context['myPosition'] = "OUT"
        else:
            context['is_to_pay'] = False
            context['info'] = balance.objects.get(which_user=request.user)
            context['to_show'] = not (temp_ref.left_child and temp_ref.right_child)
            context['code'] = invivation.objects.get(invited_by=request.user).code

            if tree_data.objects.filter(node=request.user).exists():
                user_find = tree_data.objects.get(node=request.user)
                root = None
                temp_parent = user_find.parent

                if not temp_parent:
                    root = user_find
                else:
                    while temp_parent.parent is not None:
                        temp_parent = temp_parent.parent
                        # print(user_find.parent.node.username)

                    root = temp_parent

                myTree = binaryTree(root)

                total_nodes = myTree.count_nodes()

                context['to_show'] = context['to_show'] and total_nodes < 15
            
                temp_l = myTree.traverse_bf()
                container = []

                for i in range(0, len(temp_l)):
                    focused_object = tree_data.objects.get(node=getPerson(int(temp_l[i])))
                    if i == 0:
                        focused_object.level = 'static/img/water.png'
                    elif i > 0 and i < 3:
                        focused_object.level = 'static/img/earth.png'
                    elif i > 2 and i < 7:
                        focused_object.level = 'static/img/air.png'
                    else:
                        focused_object.level = 'static/img/fire.png'

                    if getPerson(int(temp_l[i])) == request.user:
                        context['myPosition'] = focused_object.level.split("/")[-1].split(".")[0]
                    
                    container.append(focused_object)

                context['TREE'] = container

                if context['myPosition']=="fire":
                    context['to_show'] = False
                    context['root_id'] = root.id
                    context['is_to_pay'] = not balance.objects.get(which_user=request.user).is_paid
                    # checking if user is in fire level , + is he paid ?

                if gift_record.objects.filter(TO=tree_data.objects.get(id=root.id)).exists():
                    total_gifts_collected = gift_record.objects.filter(TO=tree_data.objects.get(id=root.id)).count()
                else:
                    total_gifts_collected = 0
                
                context['total_gifts_collected'] = total_gifts_collected
                print(context['is_to_pay'])

                # print('total_nodes =', total_nodes)
                # print("===========")
                


 

    return render(request, 'main.html', context)

def collect_points(request):
    output = {}
    if request.user.is_authenticated:
        if request.method == 'GET' and request.is_ajax():
            tree_data_instance = tree_data.objects.filter(is_root=True, node=request.user)[0]
            # print(tree_data_instance)
            target_parent_node = all_parent_nodes.objects.get(parent_node=tree_data_instance)
            target_parent_node.is_out = True
            target_parent_node.save()

            target_holder = points_holder.objects.get(which_tree=tree_data_instance)
            target_holder.is_collected = True
            target_holder.save()

            print(target_parent_node)

            output['msg'] = "Amount has been collected, You have come out from the flower!"
            output['status'] = 1
            return JsonResponse(output)

    return JsonResponse({'msg': 'aha'})

def send_gifting(request):
    output = {}
    try:
        if request.user.is_authenticated:
            if request.method == 'GET' and request.is_ajax():
                root_id = int(request.GET['root_id'])

                current_balance = balance.objects.get(which_user=request.user).points
                main_qty = points_criteria.objects.all()[0].gift_points_qty

                new_gift_record = gift_record(
                    FROM = tree_data.objects.get(node=request.user),
                    TO = tree_data.objects.get(id=root_id),
                    POINTS = main_qty
                )

                new_gift_record.save()

                output['remaining_balance'] = current_balance - main_qty 
                output['status'] = 1
                output['msg'] = "Git has been sent!"
    except:
        output['status'] = 0
        output['msg'] = "Something went wrong"
    
    return JsonResponse(output)

def makeAccount(request):
    if request.method == "POST":
        if 'inviteId' not in request.POST:
            print()
            messages.info(request, "Invalid invitation link! you have not registered")
            return redirect("index")

        name = request.POST['name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        pic = request.FILES['image']
        inviteId = request.POST['inviteId']

        context = {
            "name":name,
            "l_name":l_name,
            "email":email,
            "pass1":pass1,
            "pass2":pass2,
            "inviteId":inviteId
        }

        if pass1==pass2:
            if User.objects.filter(username=email).exists():
                print("Email already taken")
                messages.info(request, "Entered email already in use!")
                context['border'] = "email" 
                return render(request, "signup.html", context)

            user = User.objects.create_user(username=email, first_name=name, email=str(pic), password=pass1, last_name=l_name)
            user.save()

            new_profile_pic = proflePics(which_user=user, pic=pic)
            new_profile_pic.save()

            increase_people = invivation.objects.get(code=inviteId)
            provider = increase_people.invited_by
            increase_people.all_registrations += 1
            increase_people.save()

            new_invitation_record = invitation_record(registered_user=user, invited_by=provider)
            new_invitation_record.save()

            new_balance = balance(
                which_user = user,
                points = points_criteria.objects.all()[0].gift_points_qty
            )

            new_balance.save()

            new_invitation = invivation(
                invited_by = user,
                code = generate_code(email),
            )

            new_invitation.save()

            if not provider.is_superuser:
                main_parent = tree_data.objects.get(node=provider)

                new_tree_node = tree_data(
                    node = user,
                    parent = main_parent
                )

                new_tree_node.save()

                if main_parent.left_child is None:
                    main_parent.left_child = new_tree_node
                    
                elif main_parent.right_child is None:
                    main_parent.right_child = new_tree_node
                
                main_parent.save()
            
            return redirect("login")
        else:
            messages.info(request, "Your pasword doesn't match!")
            context['border'] = "password"
            return render(request, "signup.html", context)


def getPerson(id):
    return User.objects.get(id=id)


# add first tree
def add_first_tree(request):
    output = {}
    if request.method=='GET' and request.is_ajax():
        try:
            LIST = json.loads(request.GET['LIST'])
            
            # print_stuff(LIST)
            for i in LIST:
                userID = int(i[1])
                print(userID)
                new_tree_node = tree_data(node = getPerson(userID))
                new_tree_node.save()

            print_stuff(LIST)

            output['status'] = 1
            output['message'] = 'First tree has been added successfully, All operations will be done automatically now!'

        except:
            output['status'] = 0
            output['message'] = "Something went wrong"
        return JsonResponse(output)

def print_stuff(a):
    for i in range(0, len(a)):
        parent_index = (i-1)/2

        if parent_index >= 0:
            parent_index = int(parent_index)
            if parent_index in range(len(a)):
                parent = int(a[parent_index][1])
        else:
            parent = None
            

        
        left_index = (2*i+1)
        right_index = (2*i+2)

        if left_index in range(len(a)):
            left = int(a[left_index][1])
        else:
            left = None
            
        if right_index in range(len(a)):
            right = int(a[right_index][1])
        else:
            right = None

        Node = int(a[i][1])

        get_perticular_node = list(tree_data.objects.filter(node = getPerson(Node)))[0]

        if left:
            get_perticular_node.left_child = list(tree_data.objects.filter(node = getPerson(left)))[0]
        
        if right:
            get_perticular_node.right_child = list(tree_data.objects.filter(node = getPerson(right)))[0]

        if parent:
            get_perticular_node.parent = list(tree_data.objects.filter(node = getPerson(parent)))[0]

        get_perticular_node.save()
        
        print("Node={}, Left={}, Right={}, Parent={}".format(Node, left, right, parent))


# function for signup

def signup(request):
    if 'inviteId' not in request.GET or request.user.is_authenticated:
        return redirect("index")
    
    if 'inviteId' in request.GET:
        try:
            checking = invivation.objects.filter(code=request.GET['inviteId'], is_disable=False).exists()
            if not checking:
                return redirect("index")
        except:
            return redirect("index")
        
    # print(request.GET['inviteId'])
    
    return render(request, "signup.html")


# function for login

def login(request):

    # parenting = User.objects.get(username="umer@gmail.com")
    # print(parenting)

    # childing = User.objects.get(username="shehzad@gmail.com")
    # print(childing)

    # main_parent = tree_data.objects.get(node=parenting)

    # main_child = tree_data.objects.get(node=childing)


    # main_parent.left_child = main_child
        
 
    # main_parent.save()

    # new_tree_NODE.save()
    

    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            messages.info(request, "Incorrect login details!")
            return redirect("login")
    else:
        return render(request, "login.html")


# function for logout

def logout(request):
    auth.logout(request)
    return redirect("index")


def adminPage(request):
    if request.user.is_authenticated and request.user.is_superuser:
        invitation_link = invivation.objects.get(invited_by=request.user).code
        context = {
            'code': invitation_link
        }

        context['all_persons'] = invitation_record.objects.filter(invited_by=request.user)
        context['total_initial_persons'] = context['all_persons'].count()
        message = False

        for i in context['all_persons']:
            if tree_data.objects.filter(node=i.registered_user).exists():
                message = True
                break

        context['all_added'] = message
        print(message)
        return render(request, 'adminpage.html', context)
    else:
        return redirect("index")

def generate_code(email_of_user):    
    CHAR = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    code = email_of_user
    code_hash = hl.md5(code.encode())
    code_hash = code_hash.hexdigest()
    both = (code, code_hash)
    print(both)
    return both[1]
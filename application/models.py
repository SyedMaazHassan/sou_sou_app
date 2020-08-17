from django.db import models
from datetime import datetime
from django.contrib.auth.models import User, auth
# Create your models here.



class proflePics(models.Model):
    which_user = models.ForeignKey(User, on_delete=models.CASCADE)
    pic = models.ImageField(upload_to='photos')

class tree_data(models.Model):
    node = models.ForeignKey(User, on_delete=models.CASCADE, related_name='main_node')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='node_parent', default=None, null=True)
    left_child = models.ForeignKey('self', on_delete=models.CASCADE, related_name='node_left_child', default=None, null=True)
    right_child = models.ForeignKey('self', on_delete=models.CASCADE, related_name='node_right_child', default=None, null=True)
    is_root = models.BooleanField(default=False)
    is_out = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.parent:
            self.is_root = True

            if not all_parent_nodes.objects.filter(parent_node=self).exists():

                main_tree = all_parent_nodes(
                    parent_node=self
                )
                main_tree.save()

        else:
            self.is_root = False

        if self.is_root and self.is_out:
            LEFT_CHILD = self.left_child
            LEFT_CHILD.parent = None
            LEFT_CHILD.save()

            RIGHT_CHILD = self.right_child
            RIGHT_CHILD.parent = None
            RIGHT_CHILD.save()
        
        super(tree_data, self).save(*args, **kwargs)

    def __str__(self):
        return self.node.username

class invivation(models.Model):
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=32)
    all_registrations = models.IntegerField(default=0)
    is_disable = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.invited_by.is_superuser:
            if self.all_registrations >= 15:
                self.is_disable = True
        else:
            if self.all_registrations >= 2:
                self.is_disable = True    
                
        super(invivation, self).save(*args, **kwargs)

class invitation_record(models.Model):
    registered_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invitation_receiver")
    invited_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invitation_provider")

class gift_record(models.Model):
    FROM = models.ForeignKey(tree_data, on_delete=models.CASCADE, related_name='provider')
    TO = models.ForeignKey(tree_data, on_delete=models.CASCADE, related_name='receiver')
    POINTS = models.FloatField()
    DATE = models.DateField(default=datetime.today().strftime('%Y-%m-%d'))
    TIME = models.TimeField(default=datetime.now().time().strftime("%H:%M:%S"))

    def save(self, *args, **kwargs):
        if not self.pk:
            decrease_points =  balance.objects.get(which_user=self.FROM.node)
            decrease_points.points -= self.POINTS
            decrease_points.is_paid = True
            decrease_points.save()

            increase_holder_points = points_holder.objects.get(which_tree=self.TO)
            increase_holder_points.points += self.POINTS
            increase_holder_points.save()

        super(gift_record, self).save(*args, **kwargs)


class all_parent_nodes(models.Model):
    parent_node = models.ForeignKey(tree_data, on_delete=models.CASCADE)
    is_out = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:

            new_tree_holder = points_holder(
                which_tree = self.parent_node,
            )

            new_tree_holder.save()

        if self.is_out:
            particular_parent = self.parent_node
            particular_parent.is_out = True
            particular_parent.save()

        super(all_parent_nodes, self).save(*args, **kwargs)



class points_holder(models.Model):
    which_tree = models.ForeignKey(tree_data, on_delete=models.CASCADE)
    points = models.FloatField(default=0)
    is_collected = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_collected:
            if not sending_history.objects.filter(holding_details=self).exists():
                new_sending_history = sending_history(
                    holding_details = self,
                )
                
                new_sending_history.save()

        super(points_holder, self).save(*args, **kwargs)

class sending_history(models.Model):
    holding_details = models.ForeignKey(points_holder, on_delete=models.CASCADE)
    DATE = models.DateField(default=datetime.today().strftime('%Y-%m-%d'))
    TIME = models.TimeField(default=datetime.now().time().strftime("%H:%M:%S"))

    def save(self, *args, **kwargs):
        if not self.pk:
            particular_balace = balance.objects.get(which_user=self.holding_details.which_tree.node)
            particular_balace.points += self.holding_details.points
            particular_balace.save()

        super(sending_history, self).save(*args, **kwargs)


class points_criteria(models.Model):
    gift_points_qty = models.FloatField()

class balance(models.Model):
    which_user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.FloatField()
    is_paid = models.BooleanField(default=False)


class binaryTree:
    def __init__(self, data):
        self.node = data.node
        self.left_child = data.left_child
        self.right_child = data.right_child

    def traverse_in(self):
        if self.node.left_child is not None:
            self.node.left_child.traverse_in()

        print(self.node, end=" ")

        if self.right_child is not None:
            self.right_child.traverse_in()

    def traverse_pre(self):
        print(self.data, end=" ")

        if self.left_child is not None:
            self.left_child.traverse_pre()

        if self.right_child is not None:
            self.right_child.traverse_pre()

    def traverse_post(self):
        if self.left_child is not None:
            self.left_child.traverse_post()

        if self.right_child is not None:
            self.right_child.traverse_post()

        print(self.data, end=" ")

    def traverse_bf(self):
        nodes = [self]
        complete_list = []

        print(self.node.id, end=" ")
        complete_list.append(self.node.id)

        while nodes:
            p = nodes.pop(0)
            if p.left_child is not None:
                p_left_child = binaryTree(p.left_child)
                print(p_left_child.node.id, end=" ")
                complete_list.append(p_left_child.node.id)
                nodes.append(p_left_child)
            if p.right_child is not None:
                p_right_child = binaryTree(p.right_child)
                print(p_right_child.node.id, end=" ")
                complete_list.append(p_right_child.node.id)
                nodes.append(p_right_child)
        print()
        # return complete_list
        return complete_list
        # print(len(complete_list))

    def count_nodes(self):
        # print(self.left_child)
        if self.left_child is None and self.right_child is None:
            return 1

        left_nodes = right_nodes = 0

        if self.left_child is not None:
            mini_l = binaryTree(self.left_child)
            left_nodes = mini_l.count_nodes()

        if self.right_child is not None:
            mini_r = binaryTree(self.left_child)
            right_nodes = mini_r.count_nodes()

        return left_nodes + right_nodes + 1

    def count_leaf(self):
        if self.left_child is None and self.right_child is None:
            return 1
        left_leaves = right_leaves = 0
        if self.left_child is not None:
            left_leaves = self.left_child.count_leaf()

        if self.right_child is not None:
            right_leaves = self.right_child.count_leaf()

        return left_leaves + right_leaves
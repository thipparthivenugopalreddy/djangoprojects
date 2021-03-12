from django.contrib.auth.models import Group,User
from accounts.models import Customer
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_cus(sender, instance , created , **kwargs):
    if created:
        print("created")
        group=Group.objects.get(name="customer")
        instance.groups.add(group)
        # we now got the customer group we need to add this to the new crated user
        Customer.objects.create(customer=instance,name=instance.username)


# pre_save(create_cus,sender=User)

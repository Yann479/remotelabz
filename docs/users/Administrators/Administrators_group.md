#Group management
##Group creation

![Screenshot](/images/Administrator/group/GroupCreation.png)

Only teachers and administrators can create groups.

The creator of the group has the administrator role and he can give this role to other members of the group. 

The group has a "visibility" property. It can be :

- public
- private
- internal

All public groups and so, their associated activities, also called labs, can be view by all users of the RemoteLabz.
Internal groups can be view only by the member of the groups and the private groups can be view only by its owner. The administrator of RemoteLabz shows all groups and so, all activities.
The private group can be used to test and develop activities and as soon as the activities are ready, either the owner or the administrator of the group can change the "visibility" property to add the activities in a public or internal groups.

!!! Tip
    From version 2.4.0, each privileged user of a group (owner or administrator of a group) can add to its group, any laboratories whose he is the author. If a lab is added to a group, each member of any sub-group can also view this lab. But if a laboratory is added only to a sub-group, nobody of its parent group can see this lab.Let 3 groups, Gr1 with the two following sub-group SubGrA and SubGrB. If Lab A is affected to Gr1, so all members of SubGrA and SubGrB can execute Lab A. But if Lab B is affected to SubGrB, only members of SubGrB will execute this Lab B.

Every parameter including name, subname, visibility, description... can be changed by it's administrator(s) in the group setting panel.It is also possible to delete the group or change it's namespace from there 

##Adding user to a group

![Screenshot](/images/Administrator/group/Administrator_groupmembers.png)

.

A member of a group can have two profiles : 

 * simple user
 * administrator

The administrator of a group manages it. So, it can add members to the group, create a subgroup of this group, change the role of a member, add, or delete a member

A simple user has limited privileges; it can only view other users and interact with laboratories.

It is also possible to add multiple users to a group via a .CSV file, however it must be encoded in UTF-8 and respect the following convention.
```bash
numero;nom;prenom;email
```
It is also possible to import users from another group via the "import from group" feature.

##Adding laboratories to a group
![Screenshot](/images/Administrator/group/Administrator_GroupLaboratoriesadded.png)
If you are administrator of a group, you can add any lab to it.This will allow every registered users in this group to see the lab and start their own instance of it.

##Delete a group
![Screenshot](/images/Administrator/group/Administrator_Group_delete.png)
Only the owner can delete a group.Once deleted, the group cannot be restored.To delete a group, go to Group Setting and at the very bottom there is a delete button.

##Change namespace
![Screenshot](/images/Administrator/group/Administrator_Group_namespace.png)
Only the owner can change the namespace of a group.To do this, go to "Group Settings" and then "change namespace".From there, you can:

 - Select the namespace from another group.Once changed, the group will become a subgroup of the selected group.
 - Leave the namespace empty.This will clear the namespace.Your group will remain as it is.If it is in a subgroup, it will became an independant group.

!!! warning
    This may delete all user (except the owner) or laboratories from the group. 



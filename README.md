# Django Linear

Django app to display Linear issues via the Django admin site.

This app is designed to enable 'readonly' user access to Linear issues via the standard Django admin site.

Motivation

We replaced our use of Jira with Linear a while back, and haven't looked back - we have "Dev", "Design" and "Data" teams, and we use Linear to manage work internally. However, one thing that would improve it for our use case (small company, lots of engaged internal stakeholders) would be the ability to share the status of issues more widely through the company. This doesn't need to be sophisticated, we don't need to accept edits / comments - it's just a status update - for any issue, who is working on it, what its status is, which cycle / project it is part of. 

Approach

We have a large "backoffice" project written in Django, and all our internal staff have accounts set up, and know their way around the Django admin site. Linear has a GraphQL API. Putting these two together, it ought to be simple to be able to sync Linear updates to a Django model, and to surface those via the admin site. 

The existing Google Sheets integration is almost good enough - but it should be possible to do something a little neater.

ID | Team | Project | Milestone | Task | Estimate | Assigned to | Status
--- | --- | --- | --- | --- | --- | --- | ---
DEV-1 | Development | Flux Capacitor | Test Run | Build fuel pump | XL | Doc | In Progress
DES-1 | Design | Flux Capacitor | Investor Demo | Design logo | L | Marty | In Progress

The advantage of having the data in Django is that we a.) get filtering by default, and b.) we can start adding user-specific filters - notably subscriptions.

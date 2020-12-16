# Django Linear

Readonly access to Linear issues for users without a Linear account.

This app is designed to enable 'readonly' user access to Linear issues via the Django admin site.

### Motivation

We replaced our use of Jira with Linear a while back, and haven't looked back. However, one thing
that would improve it for our use case (small dev / design team, with many engaged internal
stakeholders) would be the ability to share the status of issues more widely through the company.

This doesn't need to be sophisticated, we don't need to accept edits / comments - it's just a status
update - for any issue, who is working on it, what its status is, which cycle / project it is part
of.

### Why bother?

The existing Google Sheets integration is almost good enough - but having the data in Django means
we can build additional functionality on top (custom notifications, alerts, reporting, etc.)

That said - this project is mainly an excuse to explore the GraphQL API.

### Approach

We have a large "backoffice" project written in Django, and all our internal staff have accounts set
up, and know their way around the Django admin site. Linear has a GraphQL API. Putting these two
together, it ought to be simple to sync Linear updates to a Django model, and to surface those via
the admin site.

![Screenshot of admin site](https://raw.githubusercontent.com/yunojuno/django-linear/master/screenshots/issue-list-view.png)

### Principles

1. Access is managed via existing Django authentication
1. Data is readonly - if someone needs to edit an issue they should use Linear
1. Users who require access to Linear should have a full ($) account

NB this is **not** a tool to bypass Linear fees. Please respect their hard work.

### How it works

The integration between Linear and the app occurs in two ways - via bulk import, and via webhook.
The data is readonly, so the principal is that all issues are imported once from Linear, and then
maintained via the webhook whenever they are updated. The webhook handler will pick up new Issues
created after the import.

The integration doesn't go too deep into the data - we store the basics only - this is only intended
for use as simple dashboard for people who don't have / need access to Linear itself.

You can import the issues via the admin site itself (there is no "Add Linear issue" button), or if
you wish you can run the `import_issues` management command. If you don't have too many issues you
could even run the import on a schedule - start afresh each day.

### Configuration

It's a standard Django app, so add it to `INSTALLED_APPS` as you would any other. The webhook URL is
`/webook/`, so the recommended configuration is to add it to your main `urls.py` like this, making
the full url `/linear/webhook/`:

```python
urlpatterns = [
    path("linear/", include("linear.urls")),
]
```

You should use this URL (with your fully-qualified domain name) when adding the webhook to Linear.

#### Settings

The following Django settings are available:

`LINEAR_API_KEY`

The only setting that is required is a valid API key, which is available from the Linear app, under
"Workspace settings" > "API" > "Personal API keys".

`LINEAR_API_PAGE_SIZE`

The page size to use when importing issues - defaults to 100, the max allowed by the API is 250.

`LINEAR_WORKSPACE_NAME`

Your workspace name is optional, but it is used in the admin site to provide a link from the object
page to Linear - overriding the Django "View on site" link.

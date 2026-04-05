from django.urls import reverse

from core.models import Project, Task


def get_link_chain(item):
    link_chain = []

    for breadcrumb in item.get_breadcrumbs():
        if isinstance(breadcrumb, Project):
            link = {
                'url': reverse('core:project', kwargs={'project_id': breadcrumb.id}),
                'text': breadcrumb.name,
            }
            link_chain.append(link)
            continue

        if isinstance(breadcrumb, Task):
            link = {
                'url': reverse('core:task', kwargs={'task_id': breadcrumb.id}),
                'text': breadcrumb.name,
            }
            link_chain.append(link)
            continue

    return link_chain

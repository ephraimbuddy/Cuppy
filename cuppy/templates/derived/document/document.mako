<%inherit file="cuppy:templates/base/base.mako"/>

<article metal:fill-slot="content" class="document-view content">
    <h1>${document.title}</h1>
    <p class="lead">
      ${document.description or ''}
    </p>
    <div class="document-body">
    ${document.body|n}
    </div>
  </article>
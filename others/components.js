/* =============================================================================
   /others/components.js
   ============================================================================= */


/* ── Patch <head> meta and mark active nav link after DOM ready ───────────── */
document.addEventListener("DOMContentLoaded", function () {
  var title = window.PAGE_TITLE       || "Ajoy Karmakar";
  var desc  = window.PAGE_DESCRIPTION || "";
  var url   = window.PAGE_URL         || "";

  document.title = title;

  function sm(sel, val) { var el = document.querySelector(sel); if (el && val) el.setAttribute("content", val); }
  function sl(sel, val) { var el = document.querySelector(sel); if (el && val) el.setAttribute("href",    val); }

  sm('meta[name="description"]',        desc);
  sm('meta[property="og:title"]',       title);
  sm('meta[property="og:description"]', desc);
  sm('meta[property="og:url"]',         url);
  sl('link[rel="canonical"]',           url);

  /* Mark active navbar link based on current URL path */
  var path = window.location.pathname;
  document.querySelectorAll("#navbar-main .nav-link").forEach(function (a) {
    var href = (a.getAttribute("href") || "").split("#")[0];
    a.classList.toggle("active", !!(href && href !== "/" && path.indexOf(href) === 0));
  });
});


/* ── 1. SEARCH OVERLAY — DISABLED ────────────────────────────────────────── */
/* To re-enable: uncomment the document.write block below.
   Also see others/search_overlay.html for full instructions.               */
function SITE_searchOverlay() {
  /* SEARCH DISABLED — uncomment below to re-enable (requires web server + index.json)

  document.write('\
<aside class="search-results" id="search">\
  <div class="container">\
    <section class="search-header">\
      <div class="row no-gutters justify-content-between mb-3">\
        <div class="col-6"><h1>Search</h1></div>\
        <div class="col-6 col-search-close">\
          <a class="js-search" href="#"><i class="fas fa-times-circle text-muted" aria-hidden="true"></i></a>\
        </div>\
      </div>\
      <div id="search-box">\
        <input name="q" id="search-query" placeholder="Search..." autocapitalize="off"\
               autocomplete="off" autocorrect="off" spellcheck="false" type="search">\
      </div>\
    </section>\
    <section class="section-search-results"><div id="search-hits"></div></section>\
  </div>\
</aside>');

  */
}


/* ── 2. NAVBAR ───────────────────────────────────────────────────────────── */
function SITE_navbar() {
  document.write('\
<nav class="navbar navbar-light fixed-top navbar-expand-lg py-0 compensate-for-scrollbar" id="navbar-main">\
  <div class="container">\
    <a class="navbar-brand" href="/">Ajoy Karmakar</a>\
    <button type="button" class="navbar-toggler" data-toggle="collapse"\
            data-target="#navbar" aria-controls="navbar" aria-expanded="false" aria-label="Toggle navigation">\
      <span><i class="fas fa-bars"></i></span>\
    </button>\
    <div class="collapse navbar-collapse" id="navbar">\
      <ul class="navbar-nav mr-auto">\
        <li class="nav-item"><a class="nav-link" href="/#research"><span>Research</span></a></li>\
        <li class="nav-item"><a class="nav-link" href="/#publications"><span>Publications</span></a></li>\
        <li class="nav-item"><a class="nav-link" href="/#experience"><span>Experience</span></a></li>\
        <li class="nav-item"><a class="nav-link" href="/#contact"><span>Contact</span></a></li>\
        <li class="nav-item"><a class="nav-link" href="/files/Ajoy_CV.pdf" target="_blank" rel="noopener noreferrer"><span>CV</span></a></li>\
      </ul>\
      <ul class="navbar-nav ml-auto">\
        <li class="nav-item">\
          <a class="nav-link js-dark-toggle" href="#"><i class="fas fa-moon" aria-hidden="true"></i></a>\
        </li>\
      </ul>\
    </div>\
  </div>\
</nav>');

  /* SEARCH ICON — uncomment the <li> below to re-enable search in navbar:

        <li class="nav-item">\
          <a class="nav-link js-search" href="#"><i class="fas fa-search" aria-hidden="true"></i></a>\
        </li>\

  */
}


/* ── 3. FOOTER ───────────────────────────────────────────────────────────── */
function SITE_footer() {
  var year = new Date().getFullYear();
  document.write('\
<div class="container">\
  <footer class="site-footer">\
    <p class="powered-by">&copy; ' + year + ' <a href="/">Ajoy Karmakar</a></p>\
    <p class="powered-by">\
      Powered by the <a href="https://sourcethemes.com/academic/" target="_blank" rel="noopener">Academic theme</a>\
      for <a href="https://gohugo.io" target="_blank" rel="noopener">Hugo</a>.\
      <span class="float-right" aria-hidden="true">\
        <a href="#" class="back-to-top"><span class="button_icon"><i class="fas fa-chevron-up fa-2x"></i></span></a>\
      </span>\
    </p>\
  </footer>\
</div>');
}




/* ── 4. CITE MODAL ───────────────────────────────────────────────────────── */
function SITE_citeModal() {
  document.write('\
<div id="modal" class="modal fade" role="dialog">\
  <div class="modal-dialog"><div class="modal-content">\
    <div class="modal-header">\
      <h5 class="modal-title">Cite</h5>\
      <button type="button" class="close" data-dismiss="modal" aria-label="Close">\
        <span aria-hidden="true">&times;</span>\
      </button>\
    </div>\
    <div class="modal-body"><pre><code class="tex hljs"></code></pre></div>\
    <div class="modal-footer">\
      <a class="btn btn-outline-primary my-1 js-copy-cite" href="#" target="_blank">\
        <i class="fas fa-copy"></i> Copy\
      </a>\
      <a class="btn btn-outline-primary my-1 js-download-cite" href="#" target="_blank">\
        <i class="fas fa-download"></i> Download\
      </a>\
      <div id="modal-error"></div>\
    </div>\
  </div></div>\
</div>');
}


/* ── 5. ALL SCRIPTS — call this LAST in <body> ───────────────────────────── */
function SITE_scripts() {
  var c = "https://cdnjs.cloudflare.com/ajax/libs/";

  /* Core scripts — always loaded */
  document.write('<script src="'+c+'jquery/3.4.1/jquery.min.js"><\/script>');
  document.write('<script src="'+c+'jquery.imagesloaded/4.1.4/imagesloaded.pkgd.min.js"><\/script>');
  document.write('<script src="'+c+'jquery.isotope/3.0.6/isotope.pkgd.min.js"><\/script>');
  document.write('<script src="'+c+'fancybox/3.5.7/jquery.fancybox.min.js"><\/script>');
  document.write('<script src="'+c+'highlight.js/9.15.10/highlight.min.js"><\/script>');
  document.write('<script src="'+c+'highlight.js/9.15.10/languages/r.min.js"><\/script>');
  document.write('<script>hljs.initHighlightingOnLoad();<\/script>');
  document.write('<script src="'+c+'leaflet/1.5.1/leaflet.js"><\/script>');
  document.write('<script src="/js/academic.min.d6bd04fdad2ad213aa8111c5a3b72fc5.js"><\/script>');

  /* SEARCH SCRIPTS — uncomment the block below to re-enable search.
     Requires: web server + /index.json (run python others/generate_index.py first).
     See others/search_overlay.html for full instructions.

  document.write('<script src="'+c+'fuse.js/3.2.1/fuse.min.js"><\/script>');
  document.write('<script src="'+c+'mark.js/8.11.1/jquery.mark.min.js"><\/script>');
  document.write('<script>\
const search_config={"indexURI":"/index.json","minLength":1,"threshold":0.3};\
const i18n={"no_results":"No results found","placeholder":"Search...","results":"results found"};\
const content_type={"post":"Posts","project":"Projects","publication":"Publications","talk":"Talks"};\
<\/script>');
  document.write('<script id="search-hit-fuse-template" type="text/x-template">\
<div class="search-hit" id="summary-{{key}}">\
<div class="search-hit-content"><div class="search-hit-name">\
<a href="{{relpermalink}}">{{title}}<\/a>\
<div class="article-metadata search-hit-type">{{type}}<\/div>\
<p class="search-hit-description">{{snippet}}<\/p>\
<\/div><\/div><\/div><\/script>');

  */
}

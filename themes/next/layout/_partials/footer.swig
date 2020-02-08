<script async src="https://busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js"></script>

<div class="copyright">{#
#}{% set current = date(Date.now(), "YYYY") %}{#
#}&copy; {% if theme.footer.since and theme.footer.since != current %}{{ theme.footer.since }} &mdash; {% endif %}{#
#}<span itemprop="copyrightYear">{{ current }}</span>
  <span class="with-love">
    <i class="fa fa-{{ theme.footer.icon }}"></i>
  </span>
  <span class="author" itemprop="copyrightHolder">{{ theme.footer.copyright || config.author }}</span>
  
  {% if theme.post_wordcount.totalcount %}
    <span class="post-meta-divider">|</span>
    <span class="post-meta-item-icon">
      <i class="fa fa-area-chart"></i>
    </span>
    {% if theme.post_wordcount.item_text %}
      <span class="post-meta-item-text">{{ __('post.totalcount') }}&#58;</span>
    {% endif %}
    <span title="{{ __('post.totalcount') }}">{#
    #}{{ totalcount(site, '0,0.0a') }}{#
  #}</span>
  {% endif %}
</div>

{% if theme.footer.powered %}
  <div class="powered-by">{#
  #}{{ __('footer.powered', 'Hexo') }}{#
  #}</div>
{% endif %}

{% if theme.footer.powered and theme.footer.theme.enable %}
  <span class="post-meta-divider">|</span>
{% endif %}

{% if theme.footer.theme.enable %}
  <div class="theme-info">{#
  #}<i class="fa fa-life-ring" aria-hidden="true"></i><span></span> {#
  #}{% if theme.footer.theme.link %}
  <a class="theme-link" target="_blank" href="https://github.com/iissnan/hexo-theme-next" rel="external nofollow">{#
    #}{% endif %} NexT.{{ theme.scheme }}{#
  #}</a>{% if theme.footer.theme.version %} v{{ theme.version }}{% endif %}{#
#}</div>
{% endif %}

{% if theme.footer.custom_text %}
  <div class="footer-custom">{#
  #}{{ theme.footer.custom_text }}{#
#}</div>
{% endif %}

<div class="theme-info">
  <span>&nbsp;|&nbsp;</span>
  <i class="fa fa-eye" aria-hidden="true"></i><span id="busuanzi_container_site_pv">&nbsp;<span id="busuanzi_value_site_pv">
  </span>&nbsp;</span>
  <i class="fa fa-user-md"></i><span id="busuanzi_container_site_uv">&nbsp;<span id="busuanzi_value_site_uv"></span>&nbsp;</span>
  <i class="fa fa-area-chart" aria-hidden="true"></i>
  <span class="post-count">Words: {{ totalcount(site) }}</span>
</div>
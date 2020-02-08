{% if page.comments %}

{% if theme.livere.enable or theme.gitalk.enable %}
  <div class="comments" id="comments">

  {% if theme.livere.enable %}
    <div id="lv-container" data-id="city" data-uid="{{ theme.livere.livere_uid }}"></div>
  {% endif %}

  {% if theme.gitalk.enable %}
    <div id="gitalk-container">
	</div>
  {% endif %}
  
  </div>
 {% endif %}

{% endif %}
---
title: 相册
date: 2019-01-04 21:47:47
type: "photos"
comments: true
livere: true
no_gitalk: true
---

<link rel="stylesheet" href="../lib/album/default-skin/default-skin.css">
<link rel="stylesheet" href="../lib/album/ins.css">
<link rel="stylesheet" href="../lib/album/photoswipe.css"> 

<iframe frameborder="no" border="0" marginwidth="0" marginheight="0" width=330 height=86 src="//music.163.com/outchain/player?type=2&id=1374416&auto=0&height=66"></iframe>
<div class="photos-btn-wrap">
    <a class="photos-btn active" href="javascript:void(0)">Photos</a>
</div>
<div class="instagram itemscope">
    <a href="#" target="_blank" class="open-ins">图片正在加载中…</a>
</div>

<script>
  (function() {
    var loadScript = function(path) {
      var $script = document.createElement('script')
      document.getElementsByTagName('body')[0].appendChild($script)
      $script.setAttribute('src', path)
	  document.getElementsByClassName('pswp__ui pswp__ui--hidden')[0].setAttribute("style", "display:block")
    }
    setTimeout(function() {
        loadScript('../lib/album/ins.js')
    }, 0)
  })()
</script>

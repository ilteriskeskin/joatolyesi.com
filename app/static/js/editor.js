// Markdown editör araç çubuğu: seçili metni sarar / satır başına ekler
(function () {
  var ta = document.querySelector(".md-editor textarea");
  var bar = document.querySelector(".md-toolbar");
  if (!ta || !bar) return;

  function wrap(before, after) {
    var s = ta.selectionStart, e = ta.selectionEnd;
    var sel = ta.value.slice(s, e) || "metin";
    ta.setRangeText(before + sel + after, s, e, "select");
    ta.setSelectionRange(s + before.length, s + before.length + sel.length);
    ta.focus();
  }
  function linePrefix(prefix) {
    var s = ta.selectionStart;
    var lineStart = ta.value.lastIndexOf("\n", s - 1) + 1;
    ta.setRangeText(prefix, lineStart, lineStart, "end");
    ta.focus();
  }

  bar.addEventListener("click", function (ev) {
    var b = ev.target.closest("button[data-md]");
    if (!b) return;
    ev.preventDefault();
    switch (b.dataset.md) {
      case "bold": wrap("**", "**"); break;
      case "italic": wrap("*", "*"); break;
      case "h2": linePrefix("## "); break;
      case "list": linePrefix("- "); break;
      case "quote": linePrefix("> "); break;
      case "link": wrap("[", "](https://)"); break;
    }
  });

  // Ctrl/Cmd+B ve I kısayolları
  ta.addEventListener("keydown", function (ev) {
    if (!(ev.metaKey || ev.ctrlKey)) return;
    if (ev.key === "b") { ev.preventDefault(); wrap("**", "**"); }
    if (ev.key === "i") { ev.preventDefault(); wrap("*", "*"); }
  });
})();

// Copied from Trac source. Remove when Trac < 1.2 is no longer supported.
// Add a Select All checkbox to each thead in the table.
if (!$.isFunction($.fn.addSelectAllCheckboxes)) {
  $.fn.addSelectAllCheckboxes = function () {
    var $table = this;
    if ($("tr td.sel", $table).length > 0) {
      $("tr th.sel", $table).append(
        $('<input type="checkbox" name="toggle_group" />').attr({
          title: _("Toggle group")
        }).click(function () {
          $("tr td.sel input",
            $(this).closest("thead, tbody").next())
            .prop("checked", this.checked).change();
        })
      );
      $("tr td.sel", $table).click(function () {
        var $tbody = $(this).closest("tbody");
        var $checkboxes = $("tr td.sel input", $tbody);
        var num_selected = $checkboxes.filter(":checked").length;
        var none_selected = num_selected === 0;
        var all_selected = num_selected === $checkboxes.length;
        $("tr th.sel input", $tbody.prev())
          .prop({
            "checked": all_selected,
            "indeterminate": !(none_selected || all_selected)
          });
      });
    }
  };
}

$(function() {
    dhcp_toggle();
    $("input#dhcp").click(dhcp_toggle);
});

function dhcp_toggle() {
    $("div#static_ip_fields :input").prop("disabled", $("input#dhcp").prop("checked"));
}

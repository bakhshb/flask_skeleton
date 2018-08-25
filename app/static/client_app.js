//bootstrap WYSIHTML5 - text editor
$(".textarea").summernote({
  airMode:false,
  height: 300,
  toolbar: [
    // [groupName, [list of button]]
    ['style', ['bold', 'italic', 'underline', 'clear']],
    ['font', ['strikethrough',]],
    ['para', ['ul', 'ol', 'paragraph']],
    ['height', ['height']],
    ['insert',['picture','link']]
  ],
  popover: {
         image: [],
         link: [],
         air: []
       }
});

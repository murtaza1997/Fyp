

var scannerInput;
    $(document).scannerDetection({

        timeBeforeScanTest: 200,
        avgTimeByChar: 40,
        endChar: [13],
        onComplete: function(barcode, qty) {
            scannerInput = barcode;
            console.log(scannerInput)
            var element=`<tr><th scope="row"><input type="checkbox" /></th><td class="tm-product-name">`+scannerInput+`</td><td>2,000</td><td>400</td><td>21 Jan 2019</td><td><a href="#" class="tm-product-delete-link"><i class="far fa-trash-alt tm-product-delete-icon"></i></a></td></tr>`
            $("#posBody").append(element)
        }
    });


$("#Addbtn").on("click",function(e){
    e.preventDefault();
    var element=`<tr><th scope="row"><input type="checkbox" /></th><td class="tm-product-name">Lorem Ipsum Product 11</td><td>2,000</td><td>400</td><td>21 Jan 2019</td><td><a href="#" class="tm-product-delete-link"><i class="far fa-trash-alt tm-product-delete-icon"></i></a></td></tr>`
    $("#posBody").append(element)
});


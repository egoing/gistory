<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <title>Gistory</title>

    <!-- Bootstrap -->
    <link href="/static/bootstrap/3.3.4/css/bootstrap.min.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
      <script src="/static/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="/static/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
    <link href="/static/css/font.css" rel="stylesheet">
    <link rel="stylesheet" href="/static/style.css"/>
    <link rel="stylesheet" href="/static/lity.min.css"/>
  </head>
  <body>
    <div class="container-fluid">
      <div class="page-header">
        <h1>Gistory</h1>
        <a href="https://www.youtube.com/playlist?list=PLuHgQVnccGMC6_JRFarkLPBfSNFwrGVlJ" target="_blank" class="manual"><span>help</span></a>
      </div>
      <div class="container">
        <div class="element-list">
            <div class="list-group">
                % for item in elements:
                    <a  href="#viewer"
                        class="list-group-item element"
                        data-path="{{item[0]}}">
                        <span class="time">{{item[1]}}</span>
                        <span class="path">{{item[0][item[0].find('.git')+5:]}}<span></span>
                    </a>
                % end
            </div>
        </div>
        <div class="viewer" id="viewer">
        </div>
      </div>
    </div>
    <!-- jQuery (necessary for Bootstrap's JavaScript plugins) -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    <!-- Include all compiled plugins (below), or include individual files as needed -->
    <script src="/static/bootstrap/3.3.4/js/bootstrap.min.js"></script>
    <script src="/static/script.js"></script>
    <script src="/static/lity.min.js"></script
  </body>
</html>

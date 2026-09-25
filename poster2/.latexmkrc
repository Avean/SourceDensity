# Compile poster.tex with XeLaTeX (fontspec needs XeLaTeX or LuaLaTeX, not pdfLaTeX)
$pdf_mode = 5;
$xelatex = "xelatex -synctex=1 -interaction=nonstopmode -file-line-error %O %S";

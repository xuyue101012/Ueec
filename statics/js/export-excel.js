//获得浏览器
function getExplorer() { 
	var explorer = window.navigator.userAgent ; 
	 //ie 
	if (explorer.indexOf("MSIE") >= 0||!!window.ActiveXObject || "ActiveXObject" in window) { 
	  return 'ie'; 
	} 
	//firefox 
	else if (explorer.indexOf("Firefox") >= 0) { 
	  return 'Firefox'; 
	} 
	//Chrome 
	else if(explorer.indexOf("Chrome") >= 0){ 
		return 'Chrome'; 
	} 
	  //Opera 
	else if(explorer.indexOf("Opera") >= 0){ 
		return 'Opera'; 
	} 
	  //Safari 
	else if(explorer.indexOf("Safari") >= 0){ 
		return 'Safari'; 
	} 
}
//导出table内容为Excel
 function exporttable(element){ 
	  if(getExplorer()=='ie') 
	  { 
	//  var curTbl = document.getElementById(tableid); 
	  var curTbl = element; 
					var oXL = new ActiveXObject("Excel.Application"); 
					var oWB = oXL.Workbooks.Add(); 
					var oSheet = oWB.ActiveSheet; 
					var Lenr = curTbl.rows.length; 
					for (i = 0; i < Lenr; i++) 
					{ var Lenc = curTbl.rows(i).cells.length; 
						for (j = 0; j < Lenc; j++) 
						{ 
							oSheet.Cells(i + 1, j + 1).value = curTbl.rows(i).cells(j).innerText; 
		 
						} 
		 
					} 
					oXL.Visible = true; 
	  } 
	  else 
	  { 
	  tableToExcel(element) 
	  } 
 } 
 var tableToExcel = (function() { 
	  var uri = 'data:application/vnd.ms-excel;base64,', 
	   template = '<html><head><meta charset="UTF-8"></head><body><table>{table}</table></body></html>', 
	   base64 = function(s) { return window.btoa(unescape(encodeURIComponent(s))) }, 
	   format = function(s, c) { 
	   return s.replace(/{(\w+)}/g, 
		function(m, p) { return c[p]; }) } 
	  return function(element, name) { 
	//  if (!table.nodeType) table = document.getElementById(table) 
	  if (!element.nodeType) element = element 
	  var ctx = {worksheet: name || 'Worksheet', table: element.innerHTML} 
	  window.location.href = uri + base64(format(template, ctx)) 
  } 
 })() 

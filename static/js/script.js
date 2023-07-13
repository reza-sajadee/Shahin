/*
 ********************************************
 * Author 	: Amir Shokri					*
 * Email 	: amirsh.nll@gmail.com 			*
 * Website	: www.amirshnll.ir 				*
 * Date 	: 2020, May 					*
 * Location : Iran, Tehran 					*
 ********************************************
 */

/* Convert Numbers */
function convert_number_to_persian(myString) {
    numbers = {
    	0: '۰',
    	1: '۱',
    	2: '۲',
    	3: '۳',
    	4: '۴',
    	5: '۵',
    	6: '۶',
    	7: '۷',
    	8: '۸',
    	9: '۹'
	};
	myString = myString.toString();
	myString = myString.trim();
	return myString.replace(/[0-9]/g, function(w){ return numbers[w] });
}
function convert_number_to_english(myString) {
    numbers = {
    	0: '0',
    	1: '1',
    	2: '2',
    	3: '3',
    	4: '4',
    	5: '5',
    	6: '6',
    	7: '7',
    	8: '8',
    	9: '9'
	};
	myString = myString.toString();
	myString = myString.trim();
	return myString.replace(/[0-9]/g, function(w){ return numbers[w] });
}


/* Close Widget */
function close_widget() {
	document.getElementById("widget").classList.add("d-none");
	return;
}

/* Show Time */
function show_time(){
	d=new Date();
	H=d.getHours();H=(H<10)?"0"+H:H;
	i=d.getMinutes();i=(i<10)?""+i:i;
	s=d.getSeconds();s=(s<10)?""+s:s;
	document.getElementById('time').innerHTML = this.convert_number_to_persian(H) +":"+ this.convert_number_to_persian(i) +":"+ this.convert_number_to_persian(s);
	setTimeout("show_time()",1000);
}
show_time();

/* Show Date */
function gregorian_to_jalali(gy,gm,gd){
	g_d_m=[0,31,59,90,120,151,181,212,243,273,304,334];
	jy=(gy<=1600)?0:979;
	gy-=(gy<=1600)?621:1600;
	gy2=(gm>2)?(gy+1):gy;
	days=(365*gy) +(parseInt((gy2+3)/4)) -(parseInt((gy2+99)/100)) +(parseInt((gy2+399)/400)) -80 +gd +g_d_m[gm-1];
	jy+=33*(parseInt(days/12053));
	days%=12053;
	jy+=4*(parseInt(days/1461));
	days%=1461;
	jy+=parseInt((days-1)/365);
	if(days > 365)days=(days-1)%365;
	jm=(days < 186)?1+parseInt(days/31):7+parseInt((days-186)/30);
	jd=1+((days < 186)?(days%31):((days-186)%30));
	return [jy,jm,jd];
}
function show_date(){
	d=new Date();
	g_y=d.getFullYear();
	g_m=d.getMonth()+1;
	g_d=d.getDate();
	shamsi=gregorian_to_jalali(g_y,g_m,g_d);
	var month = new Array(12);
	month[1] = "فروردین";
	month[2] = "اردیبهشت";
	month[3] = "خرداد";
	month[4] = "تیر";
	month[5] = "مرداد";
	month[6] = "شهریور";
	month[7] = "مهر";
	month[8] = "آبان";
	month[9] = "آذر";
	month[10] = "دی";
	month[11] = "بهمن";
	month[12] = "اسفند";
	document.getElementById('date').innerHTML= this.convert_number_to_persian(shamsi[2])+" "+ month[shamsi[1]]+" "+ this.convert_number_to_persian(shamsi[0]);
	setTimeout("show_date()",60000);
}
show_date();

function get_day() {
	var d = new Date();
	var weekday = new Array(7);
	weekday[0] = "یکشنبه";
	weekday[1] = "دوشنبه";
	weekday[2] = "سه شنبه";
	weekday[3] = "چهارشنبه";
	weekday[4] = "پنجشنبه";
	weekday[5] = "<span style='color:#f00;'>جمعه</span>";
	weekday[6] = "شنبه";

	var n = weekday[d.getDay()];
	document.getElementById("day").innerHTML = n;
}
get_day();

function get_gregorian(){
	d=new Date();
	g_y=d.getFullYear();
	g_m=d.getMonth()+1;
	g_d=d.getDate();
	var month = new Array(12);
	month[1] = "January";
	month[2] = "February";
	month[3] = "March";
	month[4] = "April";
	month[5] = "May";
	month[6] = "June";
	month[7] = "July";
	month[8] = "August";
	month[9] = "September";
	month[10] = "October";
	month[11] = "November";
	month[12] = "December";
	document.getElementById('gregorian').innerHTML= g_d + " " + month[g_m] + ", " + g_y;
}
get_gregorian();

function sind(x){return(Math.sin(Math.PI/180.0*x));}
function cosd(x){return(Math.cos(Math.PI/180.0*x));}
function tand(x){return(Math.tan(Math.PI/180.0*x));}
function atand(x){return(Math.atan(x)*180.0/Math.PI);}
function asind(x){return(Math.asin(x)*180.0/Math.PI);}
function acosd(x){return(Math.acos(x)*180.0/Math.PI);}
function sqrt(x){return(Math.sqrt(x));}
function frac(x){return(x%1);}
function floor(x){return(Math.floor(x));}
function ceil(x){return(Math.ceil(x));}
function loc2hor(z,d,p){return(acosd((cosd(z)-sind(d)*sind(p))/cosd(d)/cosd(p))/15);}
function Round(x,a){
	var tmp=x%a;
	if(tmp<0)
		tmp+=a;
	return(tmp);
}
function hms(x,r){
	ndt=new Date();
 	gy=ndt.getFullYear(); gm=ndt.getMonth()+1; gd=ndt.getDate();
	j_date=gregorian_to_jalali(gy,gm,gd);
	jy=j_date[0];
	jm=j_date[1];
	jd=j_date[2];
 	var m=jm;
	var d=eval(jd);
	doy=(m<6)?(m*31)+d-1:((m-6)*30)+d+185;
	if(doy>0 && doy<185)x++;
	if(x>=24)x-=24;
	h = parseInt(x);
	d60=(x-h)*60;
	m = parseInt(d60); mr=Math.round(d60);
	s = parseInt(((d60)-m)*60);
	return(((h<10)?'0':'')+h+':'+( (r==1) ? (((mr<10)?'0':'')+mr) : (((m<10)?'0':'')+m+':'+((s<10)?'0':'')+s) ));
}
function sun(m,d,h,lg){
	if(m<7)
		d= 31*(m-1)+d+h/24;
	else
		d=6+30*(m-1)+d+h/24;
	var M=74.2023+0.98560026*d;
	var L=-2.75043+0.98564735*d;
	var lst=8.3162159+0.065709824*Math.floor(d)+1.00273791*24*(d%1)+lg/15;	
	var e=0.0167065;
	var omega=4.85131-0.052954*d;
	var ep=23.4384717+0.00256*cosd(omega);
	var ed=180.0/Math.PI*e;
	var u=M;
	for(var i=1;i<5;i++)
		u=u-(u-ed*sind(u)-M)/(1-e*cosd(u));
	var v=2*atand(tand(u/2)*Math.sqrt((1+e)/(1-e)));
	var theta=L+v-M-0.00569-0.00479*sind(omega);
	var delta=asind(sind(ep)*sind(theta));
	var alpha=180.0/Math.PI*Math.atan2(cosd(ep)*sind(theta),cosd(theta));
	if(alpha>=360)
		alpha-=360;
	var ha=lst-alpha/15;
	var zohr=Round(h-ha,24);
	return ([zohr,delta]);
}
function get_holy_time(){
	ndt=new Date();
 	gy=ndt.getFullYear(); gm=ndt.getMonth()+1; gd=ndt.getDate();
	j_date=gregorian_to_jalali(gy,gm,gd);
	jy=j_date[0];
	jm=j_date[1];
	jd=j_date[2];

	var m=jm;
	var d=eval(jd);
	var lg=eval(51.43);
	var lat=eval(35.67);
	hide_seconds=1;

	var ep=sun(m,d,4,lg);
	var zohr=ep[0];
	delta=ep[1];
	ha=loc2hor(107.695,delta,lat);
	var sobh=Round(zohr-ha,24);
	ep=sun(m,d,sobh,lg);
	zohr=ep[0];
	delta=ep[1];
	ha=loc2hor(107.695,delta,lat);
	var sobh=Round(zohr-ha,24);
	document.getElementById('azansobh').innerHTML=convert_number_to_persian(hms(sobh,hide_seconds));
	ep=sun(m,d,6,lg);
	zohr=ep[0];
	delta=ep[1];
	ha=loc2hor(90.833,delta,lat);
	var toloo=Round(zohr-ha,24);
	ep=sun(m,d,toloo,lg);
	zohr=ep[0];
	delta=ep[1];
	ha=loc2hor(90.833,delta,lat);
	toloo=Round(zohr-ha,24);
	document.getElementById('toloaftab').innerHTML=convert_number_to_persian(hms(toloo,hide_seconds));
	ep=sun(m,d,12,lg);
	ep=sun(m,d,ep[0],lg);
	zohr=ep[0];
	document.getElementById('azanzohr').innerHTML=convert_number_to_persian(hms(zohr,hide_seconds));
	ep=sun(m,d,18,lg);
	zohr=ep[0];
	delta=ep[1];
	ha=loc2hor(90.833,delta,lat);
	var ghoroob=Round(zohr+ha,24);
	ep=sun(m,d,ghoroob,lg);
	zohr=ep[0];
	delta=ep[1];
	ha=loc2hor(90.833,delta,lat);
	ghoroob=Round(zohr+ha,24);
	//document.getElementById('ghoroob').innerHTML=hms(ghoroob,hide_seconds);
	ep=sun(m,d,18.5,lg);
	zohr=ep[0];
	delta=ep[1];
	ha=loc2hor(94.5,delta,lat);
	var maghreb=Round(zohr+ha,24);
	ep=sun(m,d,maghreb,lg);
	zohr=ep[0];
	delta=ep[1];
	ha=loc2hor(94.5,delta,lat);
	maghreb=Round(zohr+ha,24);
	document.getElementById('azanmaghrebasha').innerHTML=convert_number_to_persian(hms(maghreb,hide_seconds));
	document.getElementById('nimeshabeshari').innerHTML =convert_number_to_persian(hms(((sobh+ghoroob+24)/2),hide_seconds));
}
get_holy_time();

function get_jalali_month(){
	d=new Date();
	g_y=d.getFullYear();
	g_m=d.getMonth()+1;
	g_d=d.getDate();
	shamsi=gregorian_to_jalali(g_y,g_m,g_d);
	return shamsi[1];
}
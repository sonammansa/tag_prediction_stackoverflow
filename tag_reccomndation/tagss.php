<?php
ini_set('max_execution_time', 14400);
// Create connection
$con=mysqli_connect("","root","","major");
// Check connection
  
  if (mysqli_connect_errno($con))
  {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
  }
  
$sql = "select tags from posts";
if (!mysqli_query($con,$sql))
  {
  die('Error: ' . mysqli_error($con));
  } 
else
{
	$res=mysqli_query($con,$sql);
	//print_r ($res);
	//$row = mysqli_fetch_array($res,MYSQLI_ASSOC);
	//print_r ($row);
	$k=0;
  foreach($res as $r)
  {
  
  //echo $r['tags'];
  $t=explode(',',$r['tags']);
  $i= sizeof($t)-1;
  for($j=0;$j<$i;$j++)
	{
	$k++;
	$sql = "insert into tags values(".$k.",'".$t[$j]."')";
	if (!mysqli_query($con,$sql))
		{
		$k--;
		//die('Error: ' . mysqli_error($con));
		} 
	
	}
  //echo "____________________";
  }
 }
?>
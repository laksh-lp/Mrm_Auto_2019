#include <iostream>
#include <math.h>
#define epsilon 0.0000001
using namespace std;
 int main()
{
  int gear[1024];
  for(int i=0;i<10;i++)
		for(int j=i*102.4;j<i*102.4+102.4;j++)
		gear[j]=i+1;
    for(int i=0;i<1024;i++)
    cout<<gear[i]<<endl;
  }

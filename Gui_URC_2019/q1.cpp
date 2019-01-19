#include<iostream>
using namespace std;

int largest(int a[],int n)
{
  static int m=0,l=1;
if(l>=n-1)
return m;
  if(a[l]>a[m])
{
    m=l;
    l++;
    return largest(a,n);
}
}

int main()
{
  cout<<"Enter number of elements";
  int n;
  cin>>n;
  int a[n];
  cout<<"Enter elements";
  for(int i=0;i<n;i++)
  cin>>a[n];
  int m=largest(a,n);
  cout<<a[m];

}

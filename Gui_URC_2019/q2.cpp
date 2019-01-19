#include<iostream>
#include<stdio.h>
#include<string.h>
using namespace std;
void exc(int a[], int b[],int n)
{
  for(int i=0;i<n;i++)
  {
    int temp=a[i];
    a[i]=b[i];
    b[i]=temp;
  }
}
int main()
{
  cout<<"Enter number of students";
  int n;
  cin>>n;
  int a[n][5];
  char name[n][100];
  cout<<"Enter name, roll no, marks in 3 subjects seperated by spaces";
  for(int i=0;i<n;i++)
  fgets(name[i],100,stdin);
  for(int i=0;i<n;i++)
    {

      cin>>a[i][0]>>a[i][1]>>a[i][2]>>a[i][3];
      a[i][4]=(a[i][1]+a[i][2]+a[i][3]);
    }
  for(int i=0;i<n-1;i++)
  {
    for(int j=0;j<n-1;j++)
    {
      if(a[j][4]>a[j+1][4])
      {
        exc(a[j],a[j+1],5);
        char t[100];
        strcpy(t,name[j]);
        strcpy(name[j],name[j+1]);
        strcpy(name[j+1],t);
      }
    }
  }
  for(int i=0;i<n;i++)
  cout<<name[i]<<"\n";




}

	#include<iostream>
#include<math.h>
#include<stdlib.h>
#include<fstream>
#include<sstream>
#include<vector> 
#include <unistd.h>
#include<ctime>
using namespace std;

int main(int argc, char* argv[]){
cout << "TYPE: 1.filename 2.N" <<endl;

ofstream write;
write.open(argv[1]);
int N=atoi(argv[2]);

double pos[N][3];

write <<"LAMMPS data file from restart file: timestep = 0, procs = 1"<<endl;
write <<endl;

write<< 1*N << " atoms"<<endl;
write<< 1*N-1 << " bonds"<<endl;
write<< 1*N-2 << " angles"<<endl;
write <<endl;

write << 4 << " atom types" <<endl;
write << 1 << " bond types" <<endl;
write << 1 << " angle types" <<endl;
write <<endl;

write << "-50 50"  << " xlo xhi "<<endl;
write << "-50 50"  << " ylo yhi "<<endl;
write << "-50 50"  << " zlo zhi "<<endl;
write <<endl;

write << "Masses "<<endl;
write <<endl;
write << " 1 1 " <<endl;
write << " 2 1 " <<endl;
write << " 3 1 " <<endl;
write << " 4 1 " <<endl;
write <<endl;

write << "Atoms "<<endl;
write <<endl;

int n;
for(n=0;n<N;n++){
double r=1.1;

	if(n==0){
	pos[n][0]=rand()*1.0/RAND_MAX;
	pos[n][1]=rand()*1.0/RAND_MAX;
	pos[n][2]=rand()*1.0/RAND_MAX;
    }
    
    if(n>0){
    double phi=rand()*1.0/RAND_MAX*2.0*M_PI;
    double theta=rand()*1.0/RAND_MAX*M_PI;
    pos[n][0]=pos[n-1][0]+r*sin(theta)*cos(phi);
    pos[n][1]=pos[n-1][1]+r*sin(theta)*sin(phi);
    pos[n][2]=pos[n-1][2]+r*cos(theta);
    }
    //NEED TO WRITE:
    //INDEX MOLECULE TYPE X Y Z IX IY IZ
    write << n+1 << " 1 1 " << pos[n][0] << " " <<  pos[n][1] << " "  << pos[n][2] << " 0 0 0 " <<endl;
}

//CREATE BONDS BETWEEN BEADS
//THIS IS A LINEAR POLYMER SO N-1 BONDS
int nbonds=1;
write << "Bonds"<<endl;
write <<endl;
for(int n=1;n<N;n++){
write << nbonds << " " << 1  << " " << n << " " << n%N+1<<endl;
nbonds++;
}

write <<endl;

//CREATE ANGLES BETWEEN BEADS
//THIS IS A LINEAR POLYMER SO N-2 ANGLES
int nangles=1;
write << "Angles"<<endl;
write <<endl;
for(int n=0;n<N-2;n++){
if(n<N-2)write << nangles << " " << 1  << " " << n+1<< " " << n+2 << " " << n+3<<endl;
if(n==N-2)write << nangles << " " << 1  << " " << n+1 << " " << n+2 << " " << 1<<endl;
if(n==N-1)write << nangles << " " << 1  << " " << n+1 << " " << 1 << " " << 2<<endl;
nangles++;
}

return 0;
}



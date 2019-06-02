#include<iostream>
#include<list>
#include <bits/stdc++.h>
using namespace std;

struct individuo
{
	bitset<6>  	bset;
	int			num=0;		
	double		number=0;
	double 		percentage=0;	
};


list<individuo> poblacion;
float probCruzamiento=0.9;
float probMutacion=0.1;


void print(){
	list<individuo>::iterator it;
	for(it=poblacion.begin();it != poblacion.end();it++)
	{
		cout<<(*it).bset<<"\t f(x)="<<(*it).number<<"\t"<<(*it).percentage<<" %"<<endl;
	}
}

void printSinPorcentaje(){
	list<individuo>::iterator it;
	for(it=poblacion.begin();it != poblacion.end();it++)
	{
		cout<<(*it).bset<<"\t f(x)="<<(*it).number<<endl;
	}
}



double fun(double x)
{
	return x*x;
}

double generarPoblacion(int tamPoblacion)
{
	int numRand;
	for(int i=0;i<tamPoblacion;i++)
	{
		individuo one;
		numRand=rand()%64;
		one.bset=bitset<6>(numRand);		
		one.number=fun(numRand);
		poblacion.push_back(one);	
	}
}

void evaluacionIndividuos(int tamPoblacion)
{
	double total=0;
	list<individuo>::iterator it;
	for(it=poblacion.begin();it!=poblacion.end();it++)
		total+=(*it).number;
	
	for(it= poblacion.begin() ; it != poblacion.end() ; it++)
	{
		(*it).percentage = (*it).number*100.0/total;
	}
}



list<individuo>::iterator correrRuleta()
{
	int num=rand()%100;	
	int temp=0;	
	
	list<individuo>::iterator it;
	
	for(it=poblacion.begin();it != poblacion.end();it++)
	{
		temp+=(*it).percentage;
		if(num<temp)
			return it;
	}
 	return it;
}

bool correrRuletaCruce()
{
	int randNum=rand()%100;	
		
	if(randNum < probCruzamiento*100 )
		return true;

	else 
		return false;
}

bool correrRuletaMutacion()
{
	int randNum=rand()%100;	
		
	if(randNum < probMutacion*100 )
		return true;
	else 
		return false;
}





void seleccionIndividuos(int tamPoblacion)
{

	for(int i=0; i<tamPoblacion/2 ;i++)
	{
		if(correrRuletaCruce())
		{
			list<individuo>::iterator padre;
			list<individuo>::iterator madre;
			do
			{
				//Seleccionar Padre
				padre=correrRuleta();
				//Seleccionar Madre
				madre=correrRuleta();
			}
			while( padre==madre );
			
			
			cout<<"Padre :"<<(*padre).number<<endl;
			cout<<"Madre :"<<(*madre).number<<endl;	
			
			//Cruce
			//Hijo 1
			bitset<6> hijo1(0);
			hijo1[0]=(*padre).bset[0];
			hijo1[1]=(*padre).bset[1];
			hijo1[2]=(*madre).bset[2];
			hijo1[3]=(*madre).bset[3];
			hijo1[4]=(*padre).bset[4];
			hijo1[5]=(*padre).bset[5];
			
			if(correrRuletaMutacion())
			{
				hijo1[3]=!hijo1[3];
			}
			
			individuo hijo1_ind;
			hijo1_ind.bset=bitset<6>(hijo1);		
			hijo1_ind.number=fun(hijo1.to_ulong());
			hijo1_ind.percentage=0;
			poblacion.push_back(hijo1_ind);
			
			cout<<"Hijo :"<<hijo1_ind.bset <<"\t"<<"f(x)="<<hijo1_ind.number<<endl;				
			
			
			//Cruzamiento .---------------------------
			//Hijo 2
			bitset<6> hijo2(0);
			hijo2[0]=(*madre).bset[0];
			hijo2[1]=(*madre).bset[1];
			hijo2[2]=(*padre).bset[2];
			hijo2[3]=(*padre).bset[3];
			hijo2[4]=(*madre).bset[4];
			hijo2[5]=(*madre).bset[5];
			
			//Mutacion------------------------------------
			if(correrRuletaMutacion())
			{
				hijo2[3]=!hijo2[3];
			}

			individuo hijo2_ind;
			hijo2_ind.bset=bitset<6>(hijo2);		
			hijo2_ind.number=fun(hijo2.to_ulong());
			hijo2_ind.percentage=0;
			poblacion.push_back(hijo2_ind);
			cout<<"Hijo :"<<hijo2_ind.bset <<"\t"<<"f(x)="<<hijo2_ind.number<<endl<<endl;				
		}
		
	}
}


bool compare(const individuo &X, const individuo &Y)
{
	if(X.number > Y.number)
		return true;
	return false;
}

void seleccionDeSigPoblacion(int tamPoblacion)
{
	
	poblacion.sort(compare);
	while(poblacion.size() > 6)
	{
		poblacion.pop_back();
	}
}




int main()
{

	int	numIter=10;
	
	cout<<"Generacion de Pobloblcion"<<endl<<endl;
	generarPoblacion(6);
	print();
	
	for(int iter=0;iter<numIter;iter++)
	{
		cout<<"----------------------------"<<endl;
		cout<<"Iteracion N°"<<iter<<" : "<<endl;
		cout<<"Evaluacion de Individuos"<<endl<<endl;
		evaluacionIndividuos(6);
		print();
		cout<<endl<<"Seleccion de Individuos"<<endl<<endl;
		seleccionIndividuos(6);
		printSinPorcentaje();
		cout<<endl<<"Selecion de Individuos para la siguiente poblcación"<<endl<<endl;
		seleccionDeSigPoblacion(6);
		printSinPorcentaje();
		cout<<"-------------------------------"<<endl;
		
	}


	

	return 0;
}

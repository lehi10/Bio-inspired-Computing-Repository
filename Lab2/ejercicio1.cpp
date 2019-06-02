#include<iostream>
#include<list>
#include <bits/stdc++.h>
using namespace std;


struct individuo;
list<individuo *> poblacion;
int numPoblacion=10;

int	numIter=100;
int numCromosomas=5;
int limiteInf=-100;
int limiteSup=100;

float probCruzamiento=90;
float probMutacion=10;
double alpha=0.5;
int numIndividuosPorTorneo=3;


struct individuo
{
	vector<double> cromosomas;
	double				fit=0;		
	individuo(int numCromosomas)
	{
		cromosomas.resize(numCromosomas);
	}
};

void print(){
	const list<individuo>::iterator it;
	for_each(begin(poblacion) , end(poblacion),[](individuo *it){
		cout<<"[ ";
		for_each(it->cromosomas.begin(),it->cromosomas.end(),[](double crom){
			cout<<crom<<" | ";
		});
		cout<<"]\t =  ";
		cout<<(*it).fit<<endl;
	});
}

void print_individuo(individuo * one)
{
	cout<<"[ ";
	for_each(one->cromosomas.begin(),one->cromosomas.end(),[](double crom){
		cout<<crom<<" | ";
	});
	cout<<" ]"<<endl;
}



double fun(vector<double> & vec)
{
	return vec[0]-vec[1]+vec[2]-vec[3]+vec[4];
}



void generarPoblacion(int tamPoblacion, int numCromosomas, int limIzq, int limDer)
{
	int numRand;
	for(int i=0;i<tamPoblacion;i++)
	{
		individuo *one=new individuo(numCromosomas);
		
		 for(int j=0;j<numCromosomas;j++)
		 {
		 	numRand = (rand()%(abs(limIzq)+abs(limDer)))-abs(limIzq);
		 	one->cromosomas[j] = double(numRand);
		 }
		poblacion.push_back(one);	
	}
}


void evaluacionIndividuos()
{
	for_each(begin(poblacion) , end(poblacion),[](individuo *it){
		it->fit=fun(it->cromosomas);
	});
}

bool correrRuletaCruce()
{
	int randNum=rand()%100;	
	cout<<"-Valor aleatorio Cruzamiento : "<<randNum<<"  ";
	if(randNum < probCruzamiento)
	{
		cout<<" Si hay cruzamiento "<<endl;
		return true;
	}
	cout<<" No hay cruzamiento "<<endl;
	return false;
}

bool correrRuletaMutacion()
{
	int randNum=rand()%100;	
	return 	randNum < probMutacion ? true : false;
}

list<individuo *>::iterator seleccionPorTorneo(int numParaTorneo)
{
	
	list<individuo *>::iterator it_max=poblacion.end();
	map<int,bool> noRepetidosMap;
	
	while(noRepetidosMap.size() < numParaTorneo)
	{	
		int numRand=rand()%poblacion.size();		
		auto repetido = noRepetidosMap.find(numRand);	
	  	if (repetido == noRepetidosMap.end())
		{
			noRepetidosMap[numRand]=true;		
			
			list<individuo *>::iterator it = poblacion.begin();
			for(int i=0;i<numRand;i++)
				it++;
			// Torneo	
			if( it_max==poblacion.end() || (*it_max)->fit < (*it)->fit )
				it_max= it; 		
		
		}		
	}
	
 	return it_max;
}


individuo * cruzamiento_BLX(individuo* padre_1, individuo *padre_2)
{
	individuo *hijo= new individuo(padre_1->cromosomas.size());
	for(int i=0; i < padre_1->cromosomas.size();i++)
	{
		double alphaRand=alpha;
		double p1=padre_1->cromosomas[i];
		double p2=padre_2->cromosomas[i];
		hijo->cromosomas[i]=  p1+alphaRand*(p1-p2);
	}
	return hijo;
}





bool compare(individuo *X, individuo *Y)
{
	return X->fit > Y->fit ? true : false;
}

void seleccionDeSigPoblacion()
{
	poblacion.sort(compare);
	while(poblacion.size() > numPoblacion/2)
	{
		poblacion.pop_back();
	}
}


int main()
{
	cout<<"Generacion de Pobloblacion"<<endl<<endl;
	generarPoblacion(numPoblacion,numCromosomas,limiteInf,limiteSup);
	print();
	cout<<endl<<"Evaluacion de Individuos con Funcion Objetivo"<<endl<<endl;
	evaluacionIndividuos();
	print();
	
	for(int iter=0;iter<numIter;iter++)
	{
		cout<<"---------------------------------------------------------"<<endl;
		cout<<"Iteracion N°"<<iter<<" : "<<endl;
		cout<<endl<<"Seleccion de Individuos"<<endl<<endl;
		for(int i_padres=0; i_padres < poblacion.size()/2 ;i_padres++)
		{
			if(correrRuletaCruce())
			{
				list<individuo *>::iterator padre_1 =seleccionPorTorneo(numIndividuosPorTorneo); 
				list<individuo *>::iterator padre_2 =seleccionPorTorneo(numIndividuosPorTorneo); 
				cout<<"-Padre 1 :"<<endl;
				print_individuo((*padre_1));
				cout<<"-Padre 2 : "<<endl;
				print_individuo((*padre_2));
				individuo *hijo=cruzamiento_BLX(*padre_1,*padre_2);
				poblacion.push_back(hijo);
				cout<<"--Hijo"<<endl;
				print_individuo(hijo);
				cout<<endl;
			}
			
		}
		cout<<endl<<"Evaluación de Individuos"<<endl;
		evaluacionIndividuos();
		print();
		cout<<endl<<"Seleccion de Siguiente Población"<<endl;
		seleccionDeSigPoblacion();
		print();	
	}	
	return 0;
}

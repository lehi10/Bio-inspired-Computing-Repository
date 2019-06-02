#include<iostream>
#include<list>
#include <bits/stdc++.h>

using namespace std;


struct individuo;
list<individuo *> poblacion;
int	numIter=10; 
int numPoblacion=10; 
int numCromosomas=5;
float probCruzamiento=90;
float probMutacion=10;
//--------------------------

char states[5]={'A','B','C','D','E'};
map<char,map<char,double> > grafo;


struct individuo
{
	vector<char> cromosomas;
	double		fit=0;	
    double      porcentaje=0;	
	
    individuo(char camino[],int numCromosomas)
	{
        cromosomas.resize(numCromosomas);
        for(int i=0;i<numCromosomas;i++)
            cromosomas[i]=camino[i];
		
	}
};

void print(){
	const list<individuo>::iterator it;
	for_each(begin(poblacion) , end(poblacion),[](individuo *it){
		cout<<"[ ";
		for_each(it->cromosomas.begin(),it->cromosomas.end(),[](char crom){
			cout<<crom<<" | ";
		});
		cout<<"]\t =  ";
		cout<<"Fit : "<<(*it).fit<<" Porcentaje "<<(*it).porcentaje<<'%'<<endl;
	});
}

void print_individuo(individuo * one)
{
	cout<<"[ ";
	for_each(one->cromosomas.begin(),one->cromosomas.end(),[](char crom){
		cout<<crom<<" | ";
	});
	cout<<" ]"<<endl;
}

void generarPoblacion(int tamPoblacion, char camino[], int numCromosomas )
{
	for(int i=0;i<numPoblacion;i++)
    {
        next_permutation(camino,camino+numCromosomas);
        individuo *one=new individuo(camino,numCromosomas);
        poblacion.push_back(one); 
    }
}

void evaluacionIndividuos()
{
    double total_distancias=0;
    
    for_each(begin(poblacion),end(poblacion),[&total_distancias](individuo *&it_camino){
        vector<char> it_cromosomas=it_camino->cromosomas;
        double distancia=0;
        for(int i=0;i<numCromosomas;i++)
        {
            char estado_a= it_cromosomas[i%numCromosomas];
            char estado_b= it_cromosomas[(i+1)%numCromosomas];

            distancia+=grafo[estado_a][estado_b];            
        }
        it_camino->fit=distancia;
        total_distancias+=distancia;
    });

    for_each(begin(poblacion),end(poblacion),[&total_distancias](individuo *&it_camino){
        it_camino->porcentaje=(it_camino->fit*100.0)/total_distancias;
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

list<individuo*>::iterator correrRuleta()
{
	int num=rand()%100;	
	int temp=0;		
	list<individuo *>::iterator it;
	
	for(it=poblacion.begin(); it!= poblacion.end();it++)
	{
		temp+=(*it)->porcentaje;
		if(num<temp)
			return it;
	}

 	return it;
}

bool correrRuletaMutacion()
{
	int randNum=rand()%100;	
	return 	randNum < probMutacion ? true : false;
}



char PMX(map<char,char> corresp , char crom )
{
    char temp=crom;
    while( corresp.find(temp) != corresp.end() )
    {
        temp=corresp[temp];
    }
    return temp;
}


void cruzamiento_PMX(individuo *padre_1, individuo *padre_2)
{
    
    int limit_1=1;
    int limit_2=3;

    map<char,char> correspd_1;
    map<char,char> correspd_2;

    char hijo_1[numCromosomas];
    char hijo_2[numCromosomas];

    for(int i=limit_1;i<limit_2;i++)
    {
        hijo_2[i]=padre_1->cromosomas[i];
        hijo_1[i]=padre_2->cromosomas[i];

        correspd_1[padre_2->cromosomas[i]]=padre_1->cromosomas[i];
        correspd_2[padre_1->cromosomas[i]]=padre_2->cromosomas[i];
    }
    
    for(int i=0;i<limit_1;i++)
    {
        hijo_1[i]=PMX(correspd_1,padre_1->cromosomas[i]);        
        hijo_2[i]=PMX(correspd_2,padre_2->cromosomas[i]);   
    }
    
    for(int i=limit_2;i<numCromosomas;i++)
    {    
        hijo_1[i]=PMX(correspd_1,padre_1->cromosomas[i]);        
        hijo_2[i]=PMX(correspd_2,padre_2->cromosomas[i]);      
    }

    individuo *ind_hijo_1=new individuo(hijo_1,numCromosomas);
    individuo *ind_hijo_2=new individuo(hijo_2,numCromosomas);

    poblacion.push_back(ind_hijo_1);
    poblacion.push_back(ind_hijo_2);
    cout<<"----Hijo 1----"<<endl;
    print_individuo(ind_hijo_1);
    cout<<"----Hijo 2----"<<endl;
    print_individuo(ind_hijo_2);

    return ;
}


bool compare(individuo *X, individuo *Y)
{
	return X->porcentaje < Y->porcentaje ? true : false;
}

void seleccionDeSigPoblacion()
{
	poblacion.sort(compare);
	while(poblacion.size() > numPoblacion/2)
	{
		poblacion.pop_back();
	}
}


void inicializarGrafo()
{
    grafo['A']['B']=2;    grafo['A']['C']=2;
    grafo['A']['D']=1;    grafo['A']['E']=4;
    grafo['B']['C']=3;    grafo['B']['D']=2;
    grafo['B']['E']=3;    grafo['C']['D']=2;
    grafo['C']['E']=2;    grafo['D']['E']=4;
    grafo['B']['A']=2;    grafo['C']['A']=2;
    grafo['D']['A']=1;    grafo['E']['A']=4;
    grafo['C']['B']=3;    grafo['D']['B']=2;
    grafo['E']['B']=3;    grafo['D']['C']=2;
    grafo['E']['C']=2;    grafo['E']['D']=4;
}

int main()
{
    inicializarGrafo();
	cout<<"Generacion de Pobloblacion"<<endl<<endl;
	generarPoblacion(numPoblacion,states,numCromosomas);
	print();
	cout<<endl<<"Evaluacion de Individuos con Funcion Objetivo"<<endl<<endl;
	evaluacionIndividuos();
	print();
    
	for(int iter=0;iter<numIter;iter++)
	{
        cout<<"---------------------------------------------------------"<<endl;
        cout<<"Iteracion N°"<<iter<<" : "<<endl;
        cout<<endl<<"Seleccion de Individuos"<<endl<<endl;
        
		for(int i_padres=0; i_padres < numPoblacion/2  ;i_padres++)
		{
			if(correrRuletaCruce())
			{
                list<individuo *>::iterator padre;
                list<individuo *>::iterator madre;
                do
                {    
                    //Seleccionar Padre
                    padre=correrRuleta();
                    //Seleccionar Madre
                    madre=correrRuleta();
                    print_individuo(*padre);
                    print_individuo(*madre);
                }
                while( padre==madre );
                cruzamiento_PMX(*padre,*madre);
			}	
		}
        cout<<endl<<"Evaluación de Individuos"<<endl;
		evaluacionIndividuos();
		print();
		cout<<endl<<"Seleccion de Siguiente Población"<<endl;
		seleccionDeSigPoblacion();
        evaluacionIndividuos();
		print();	
	}	    
	return 0;
}


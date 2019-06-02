#include<iostream>
#include<list>
#include <bits/stdc++.h>

using namespace std;


struct individuo;
list<individuo *> poblacion;

int numPoblacion=10; 
int numCromosomas=10;


int	numIter=150;
float probCruzamiento=90;

//--------------------------

char states[10]={'A','B','C','D','E','F','G','H','I','J'};
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


void inicializarGrafo()
{
    grafo['A']['B']=12;	grafo['A']['C']=3;
    grafo['A']['D']=23; grafo['A']['E']=1;
    grafo['A']['F']=5;  grafo['A']['G']=23;
    grafo['A']['H']=56; grafo['A']['I']=12;
    grafo['A']['J']=11;
    
	grafo['B']['C']=9;  grafo['B']['D']=18;    
    grafo['B']['E']=3;  grafo['B']['F']=41;
    grafo['B']['G']=45; grafo['B']['H']=5;
    grafo['B']['I']=41; grafo['B']['J']=27;
    
    grafo['C']['D']=89; grafo['C']['E']=56;
    grafo['C']['F']=21; grafo['C']['G']=12;
    grafo['C']['H']=48; grafo['C']['I']=14;
    grafo['C']['J']=29;

    grafo['D']['E']=87; grafo['D']['F']=46;
    grafo['D']['G']=75; grafo['D']['H']=17;
    grafo['D']['I']=50; grafo['D']['J']=42;

    grafo['E']['F']=55; grafo['E']['G']=22;
    grafo['E']['H']=86; grafo['E']['I']=14;
    grafo['E']['J']=33;
    
	grafo['F']['G']=21; grafo['F']['H']=76;
    grafo['F']['I']=54; grafo['F']['J']=81;
    
    grafo['G']['H']=11; grafo['G']['I']=57;
    grafo['G']['J']=48;
    
	grafo['H']['I']=63; grafo['H']['J']=24;

	grafo['I']['J']=9;
	
	
	grafo['B']['A']=12; grafo['C']['A']=3;
    grafo['D']['A']=23; grafo['E']['A']=1;
    grafo['F']['A']=5;  grafo['G']['A']=23;
    grafo['H']['A']=56; grafo['I']['A']=12;
    grafo['J']['A']=11;
    
	grafo['C']['B']=9;  grafo['D']['B']=18;    
    grafo['E']['B']=3;  grafo['F']['B']=41;
    grafo['G']['B']=45; grafo['H']['B']=5;
    grafo['I']['B']=41; grafo['J']['B']=27;
    
    grafo['D']['C']=89; grafo['E']['C']=56;
    grafo['F']['C']=21; grafo['G']['C']=12;
    grafo['H']['C']=48; grafo['I']['C']=14;
    grafo['J']['C']=29;

    grafo['E']['D']=87; grafo['F']['D']=46;
    grafo['G']['D']=75; grafo['H']['D']=17;
    grafo['I']['D']=50; grafo['J']['D']=42;

    grafo['F']['E']=55; grafo['G']['E']=22;
    grafo['H']['E']=86; grafo['I']['E']=14;
    grafo['J']['E']=33;
    
	grafo['G']['F']=21; grafo['H']['F']=76;
    grafo['I']['F']=54; grafo['J']['F']=81;
    
    grafo['H']['G']=11; grafo['I']['G']=57;
    grafo['J']['G']=48;
    
	grafo['I']['H']=63; grafo['J']['H']=24;

	grafo['J']['I']=9;
}

bool compare(individuo *X, individuo *Y)
{
	return X->porcentaje < Y->porcentaje ? true : false;
}


void print()
{
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


void optimizacion_poblacion_inicial()
{
	poblacion.sort(compare);
	while(poblacion.size() > numPoblacion)
	{
		poblacion.pop_back();
	}
}


void generarPoblacion(int tamPoblacion, char camino[], int numCromosomas )
{
	int tam_poblacion_ini=tamPoblacion*3; //Población inicial de 3N
	
	for(int i=0;i<tam_poblacion_ini;i++)
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

	double num=(rand()%100)+((rand()%100)/100);	
	double temp=0;		
	list<individuo *>::iterator it;

	for(it=poblacion.begin(); it!= poblacion.end();it++)
	{
		temp+=(*it)->porcentaje;
		if(num<temp)
			return it;
	}
		
 	return it;
}







double  calcular_dist_ind(char *ind)
{
	char estado_a,estado_b;
    double distancia=0;
    for(int i=0;i<numCromosomas;i++)
    {
        estado_a= ind[i%numCromosomas];
        estado_b= ind[(i+1)%numCromosomas];

        distancia+=grafo[estado_a][estado_b];            
    }

    return distancia;
			
}

char* mutacion(char *ind)
{
	int i=rand()%numCromosomas;
	int j=rand()%numCromosomas;
	char temp=ind[i];
	ind[i]=ind[j];
	ind[j]=temp;
	return ind;
}

void optimizacion_local(char *ind)
{
	double temp=0;
	double dist=calcular_dist_ind(ind);
	
	char *ind_temp=new char[numCromosomas];
	cout<<"Hijo"<<endl;
	for(int i=0;i<numCromosomas;i++)
	{
		cout<<ind[i]<<" ";
		ind_temp[i]=ind[i];
	}
	cout<<endl;
	
	while(dist > temp)
	{
		temp=calcular_dist_ind(ind_temp);
		ind_temp=mutacion(ind_temp);
		dist=calcular_dist_ind(ind_temp);
	}
		
	cout<<"Optimización Local Hill Climbing"<<endl;
	for(int i=0;i<numCromosomas;i++)
	{
		ind[i]=ind_temp[i];
		cout<<ind[i]<<" ";
	}
	cout<<endl<<endl;
	
}



void cruzamiento_OBX(individuo *padre_1, individuo *padre_2)
{
    
    int limit_1=3;
    int limit_2=6;

    map<char,char> correspd_1;
    map<char,char> correspd_2;

    char hijo_1[numCromosomas];
    char hijo_2[numCromosomas];

	vector<int> marks(3);

	while(marks[0] == marks[1] || marks[0] == marks[2] || marks[2] == marks[1])
	{
		marks[0]=rand()%numCromosomas;
		marks[1]=rand()%numCromosomas;
		marks[2]=rand()%numCromosomas;
	}

	sort(marks.begin(),marks.end());
	
	cout<<marks[0]<<" - "<<marks[1]<<" - "<<marks[2]<<endl;

    for(int i=0;i<numCromosomas;i++)
    {
    	if(i!=marks[0] && i!=marks[1] && i!=marks[2])
    	{	
			hijo_1[i]=padre_1->cromosomas[i];
		    hijo_2[i]=padre_2->cromosomas[i];
    	}
    }
    
   
	
	int it_marks_1=0;
    int it_marks_2=0;
    for(int i=0;i<numCromosomas;i++)
    {
    	char it_padre_2=padre_2->cromosomas[i];
    	if(it_padre_2 == padre_1->cromosomas[marks[0]] || it_padre_2 == padre_1->cromosomas[marks[1]] || it_padre_2 == padre_1->cromosomas[marks[2]])
    	{
    		hijo_1[marks[it_marks_1]]=it_padre_2;
    		it_marks_1++;
    	}    	
    	
    	char it_padre_1=padre_1->cromosomas[i];
    	if(it_padre_1 == padre_2->cromosomas[marks[0]] || it_padre_1 == padre_2->cromosomas[marks[1]] || it_padre_1 == padre_2->cromosomas[marks[2]])
    	{
    		hijo_2[marks[it_marks_2]]=it_padre_1;
    		it_marks_2++;
    	}
    }


	optimizacion_local(hijo_1);
	optimizacion_local(hijo_2);

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


void seleccionDeSigPoblacion()
{
	poblacion.sort(compare);
	while(poblacion.size() > numPoblacion)
	{
		poblacion.pop_back();
	}
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
	cout<<"Optimización de Pobloblacion"<<endl<<endl;
	optimizacion_poblacion_inicial();
	
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
				
                cruzamiento_OBX(*padre,*madre);
        		
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


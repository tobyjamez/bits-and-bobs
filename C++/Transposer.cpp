//Matrix transposer
//Reads a matrix of arbitrary size from a comma separated .txt file and
//returns the transpose of that matrix to a .txt file.

#include <iostream>
#include <cmath>
#include <vector>
#include <string>
#include <iomanip>
#include <cstdlib>
#include <fstream>
#include <sstream>

using namespace std;

//declare main matrix vector
vector<vector<string> > m;

int main() {
	string item, line;
	int end;
	//reads input matrix file
	ifstream inputMatrix ("inputMatrix.txt");
	//isolates each line, casts it to a stringstream, and isolates each
	//element of each line
	if ( inputMatrix.is_open()){
		while( !inputMatrix.eof()){
			while( getline(inputMatrix, line, '\n')){
			vector<string> temp; //temporary vector for each line
			stringstream linestream;
			linestream << line;  //casts the line into a stream
			while( getline(linestream, item, ',')){
			temp.push_back(item);//adds each element of the line to
			}		     //the temporary vector
			m.push_back(temp);}} //adds the temporary vector to the
					     //main matrix
		inputMatrix.close();	    
		} else { //show error message
			cout << "Error, unable to open file to read\n";
			exit(1);
		}

		//declare transpose matrix vector
		vector<vector<string> > m_t(m[0].size(),vector<string>(m.size()));			
		//assign each point in the transpose matrix the relevant value
		for(int i=0; i<m.size();i++){
			for(int j=0; j<m[0].size(); j++){
				m_t[j][i] = m[i][j];
			}}
		//open file to write to and write to it
		ofstream outputMatrix ( "outputMatrix.txt" );
		if(outputMatrix.is_open()){
		for(int k=0; k<m_t.size(); k++){
			for(int l=0; l<m_t[0].size();l++){
			if(l == m_t[0].size()-1){//write a newline at the 
						 //end of each line
			outputMatrix << m_t[k][l] << '\n';
}
			else{			 //otherwise, delimit with ,
			outputMatrix << m_t[k][l] << ',';} 

}}

			outputMatrix.close();
}else{cout << "Error, unable to open file to write\n";} //error message if
							//output file can't								//be read.


		return 0;
}

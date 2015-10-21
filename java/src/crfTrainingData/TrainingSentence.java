package crfTrainingData;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.HashSet;

import property.Property;

public class TrainingSentence {
	HashSet<String> neSet = new HashSet<String>();
	Property property = Property.getInstance();
	int count = 0;
	String wpath;
	
	public void initial(String rpath,String wpath){
		try {
			this.wpath = wpath;
			String read;
			BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(wpath,true),"UTF-8")); 
			BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(rpath),"UTF-8"));
			read = br.readLine();
			for(read = br.readLine(); read!=null; read = br.readLine()){
				if(read.isEmpty()){
					bw.append("\n");
					//bw1.append("\n");
					read = br.readLine();
					continue;
				}
				String[] splits = read.split("\t");
				
				/*
				 * //only take YNO as label scheme
				 */
				if(splits.length==3){
					bw.append(splits[0]+"\tO"+"\n");
					//bw1.append(splits[2]+"\tO"+"\n");
				}else if(splits.length==4){
					if(splits[0].equals("###blank###")){
						//bw1.append(splits[2]+"\t"+splits[3]+"\n");
					}else{
						bw.append(splits[0]+"\t"+splits[1]+"\n");
						//bw1.append(splits[2]+"\t"+splits[3]+"\n");
					}
				}
			}
			br.close();
			bw.flush();
			bw.close();
			//bw1.flush();
			//bw1.close();
		} catch (Exception e) {
			// TODO: handle exception
			e.printStackTrace();
		}
	}
	
	/*
	 * count the number of positive named entities and negative named entities in the training data.
	 * return the number of positive named entities minus the number of negative named entities
	 */
	public int count(){
		try {
			BufferedReader br =  new BufferedReader(new InputStreamReader(new FileInputStream(wpath),"UTF-8"));
			String read;
			int countsentence = 0;
			int countY = 0;
			int countN = 0;
			for(read = br.readLine(); read!=null; read = br.readLine()){
				if(read.isEmpty()){
					countsentence++;
				}else{
					String[] splits = read.split("\t");
					if(splits[1].equals("Y"))
						countY++;
					else if(splits[1].equals("N")){
						countN++;
					}
				}
			}
			br.close();
			
			count = countY-countN;
			return count;
		} catch (Exception e) {
			// TODO: handle exception
			e.printStackTrace();
			return -1;
		}
	}
	
	public void control(){
		try {
			PositiveTrainingData positiveTrainingData = new PositiveTrainingData();
			positiveTrainingData.initial();
			positiveTrainingData.scan();
			positiveTrainingData.writer();
			
			Property property = Property.getInstance();
			TrainingSentence token = new TrainingSentence();
			token.initial(property.trainingSet1,property.trainingSentence);
			int count = token.count();
			NegativeTrainingData negativeTrainingData = new NegativeTrainingData(count);
			negativeTrainingData.initial();
			negativeTrainingData.scan();
			negativeTrainingData.writer();
	 		token.initial(property.trainingSet2,property.trainingSentence);
		}catch (Exception e) {
			// TODO: handle exception
			e.printStackTrace();
		}
		
		
	}
}

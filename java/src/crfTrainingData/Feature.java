package crfTrainingData;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import property.Property;

/*
 * Assign features for each word in a sentence. 
 * The features will be used in CRF.
 */

public class Feature {
	private Property property;

	
	public ArrayList<String> assignFeatures(String sentence){
		if(sentence==null)
			return null;
		ArrayList<String> list = new ArrayList<String>();
		assignFeature_O(list);
		return list;
		
	}
	
	/*
	 * G1 and G2 is about grammatical features
	 * N is about problem related features
	 * O is about lexical features
	 */
	
	
	private ArrayList<String> assignFeature_O(ArrayList<String> list){
		for(int i=0;i<list.size();i++){
			String word = list.get(i);
			String[] splits = word.split("\t");
			String feature3 = splits[0].toUpperCase();
			int feature4 = 0;
			int feature5 = 0;
			int feature6 = 0;
			int feature7 = 0;
			int feature8 = 0;
			char[] letters = splits[0].toCharArray();
			if(Character.isUpperCase(letters[0])){
				feature4 = 1;
			}
			if(splits[0].equals(splits[0].toUpperCase())){
				feature5 = 1;
			}
			int flag1 = 0;
			int flag2 = 0;
			for(char letter: letters){
				if(Character.isDigit(letter)){
					flag1 = 1;
				}else if(Character.isLetter(letter)){
					flag2 = 1;
				}
				if(Character.isUpperCase(letter)){
					feature8 = 1;
				}
			}
			if(flag1 ==1 && flag2 ==0){
				feature6 = 1;
			}else if(flag1 ==1 && flag2 ==1){
				feature7 = 1;
			}
			
			
			StringBuffer sb = new StringBuffer();
			sb.append(splits[0]);
			for(int j=1;j<splits.length;j++){
				sb.append("\t"+splits[j]);
			}
			sb.append("\t"+feature3+"\t"+feature4+"\t"+feature5+"\t"+feature6+"\t"+feature7+"\t"+feature8);
			list.set(i, sb.toString());
		}
		return list;
	}
	
	public void control(){
		try {		
			Feature feature = new Feature();
			Property property = Property.getInstance();
			BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(property.trainingSentence),"UTF-8")); 
			BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(property.trainingdata),"UTF-8"));
			String read;
			StringBuffer sb = new StringBuffer();
			ArrayList<String> list = new ArrayList<String>();
			int k = 0;
			for(read = br.readLine(); read!=null; read = br.readLine()){	
				k++;
				if(k%1000==0){
					System.out.println(k);
				}
				if(read.isEmpty()){
					ArrayList<String> featureList = feature.assignFeatures(sb.substring(0, sb.length()-1));
					for(int i=0;i<list.size();i++){
						String label = list.get(i);
						String features = featureList.get(i);
						bw.append(features+"\t"+label+"\n");
					}
					bw.append("\n");
					sb = new StringBuffer();
					list = new ArrayList<String>();
					continue;
				}
				
				String[] splits = read.split("\t");
				sb.append(splits[0]+" ");
				list.add(splits[1]);			
			}
			br.close();
			bw.flush();
			bw.close();
		} catch (Exception e) {
			// TODO: handle exception
			e.printStackTrace();
		}
	}
}

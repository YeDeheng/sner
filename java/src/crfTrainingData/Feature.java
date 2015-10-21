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

import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.ling.Sentence;
import edu.stanford.nlp.ling.TaggedWord;
import edu.stanford.nlp.tagger.maxent.MaxentTagger;

/*
 * Assign features for each word in a sentence. 
 * The features will be used in CRF.
 */

public class Feature {
	private MaxentTagger postagger;
	private HashMap<String,String> wordBrownCluster;
	private HashMap<String,Integer> itemEntropy;
	private Property property;
	
	public Feature(){
		try {
			property = Property.getInstance();
			postagger =  new MaxentTagger(property.posTagger);
			wordBrownCluster = new HashMap<String,String>();
			BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream(property.modifiedBrownCluster),"UTF-8"));
			String read;
			for(read = br.readLine(); read!=null; read = br.readLine()){
				String[] splits = read.split("\t");
				wordBrownCluster.put(splits[1], splits[0]);
			}
			br.close();
			
			
			itemEntropy = new HashMap<String,Integer>();
			br = new BufferedReader(new InputStreamReader(new FileInputStream(property.namedEntity),"UTF-8"));
			for(read = br.readLine(); read!=null; read = br.readLine()){
				String[] splits = read.split(",");
				
				int v = 0;
				double value = Double.valueOf(splits[1]);
				if(value>1){
					v = 2;
				}else{
					v = 1; 
				}
				String[] tokens = splits[0].split("\\s+");
				if(tokens.length==1){
					itemEntropy.put(splits[0],v);
				}else{
					String temp = splits[0].replaceAll(" ", "_");
					itemEntropy.put(temp,v);
				}
				
			}
			br.close();
			
			
		} catch (Exception e) {
			// TODO: handle exception
			e.printStackTrace();
		}
	}
	
	public ArrayList<String> assignFeatures(String sentence){
		if(sentence==null)
			return null;
		ArrayList<String> list = new ArrayList<String>();
		assignFeature_G1(list,sentence);
		assignFeature_G2(list);
		assignFeature_N(list);
		assignFeature_O(list);
		return list;
		
	}
	
	/*
	 * G1 and G2 is about grammatical features
	 * N is about problem related features
	 * O is about lexical features
	 */
	
	private ArrayList<String> assignFeature_G1(ArrayList<String> list,String sentence){
		//Feature_G1
		String[] splits = sentence.split("\\s+");
		List<HasWord> sent = Sentence.toWordList(splits);
		List<TaggedWord> taggedSent = postagger.tagSentence(sent);
		for (TaggedWord tw : taggedSent){
			list.add(tw.word()+"\t"+tw.tag());
		}
		return list;
	}
	
	private ArrayList<String> assignFeature_G2(ArrayList<String> list){
		for(int i=0;i<list.size();i++){
			String word = list.get(i);
			String[] splits = word.split("\t");
			String path = null;
			if(wordBrownCluster.containsKey(splits[0])){
				path = wordBrownCluster.get(splits[0]);
			}else{
				path = "null";
			}
			String feature4=null, feature6=null, feature10=null, featuer20=null;
			
			//4
			if(path.length()>4){
				feature4 = path.substring(0, 4);
			}else{
				feature4 = path;
			}
			
			//6
			if(path.length()>6){
				feature6 = path.substring(0, 6);
			}else{
				feature6 = path;
			}
			
			//10
			if(path.length()>10){
				feature10 = path.substring(0, 10);
			}else{
				feature10 = path;
			}
			
			//20
			if(path.length()>20){
				featuer20 = path.substring(0, 20);
			}else{
				featuer20 = path;
			}
			
			StringBuffer sb = new StringBuffer();
			sb.append(splits[0]);
			for(int j=1;j<splits.length;j++){
				sb.append("\t"+splits[j]);
			}
			sb.append("\t"+feature4+"\t"+feature6+"\t"+feature10+"\t"+featuer20);
			list.set(i, sb.toString());
		}
		return list;
	}
	
	private ArrayList<String> assignFeature_N(ArrayList<String> list){
		for(int i=0;i<list.size();i++){
			String word = list.get(i);
			String[] splits = word.split("\t");
			int flag1 = 0;
			int flag2 = 0;
			if(itemEntropy.containsKey(splits[0].toLowerCase())){
				flag1 = 1;
				flag2 = itemEntropy.get(splits[0].toLowerCase());
			}
			
			StringBuffer sb = new StringBuffer();
			sb.append(splits[0]);
			for(int j=1;j<splits.length;j++){
				sb.append("\t"+splits[j]);
			}
			sb.append("\t"+flag1+"\t"+flag2);
			list.set(i, sb.toString());
		}
		return list;
	}
	
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

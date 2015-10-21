package property;

import java.io.File;
import java.io.FileReader;
import java.util.Properties;

public class Property {
	private static Property property = null;
	public String engineerPath;
	public String forumData;
	public String officialname;
	public String brownCluster;
	public String brandCluster;
	public String nameCluster;
	public String brandPath;
	public String preprocessDoc;
	public String originalDoc;
	public String candidateName;
	public String stoplist;
	public int userFrequency;
	public String candidateNameStep1;
	public String candidateNameStep2Pre;
	public String candidateNameStep2;
	public String namedEntity;
	public String modifiedSentence;
	public String modifiedSearchEngineer;
	public String modifiedSearchEngineerTitle;
	public String confidenceValue;
	public String usefulNamedEntity;
	public String extendedUsedfulNamedEntity;
	public String mobilephonelist1;
	public String mobilephonelist2;
	public String absoluteConfidenceValue;
	public String mobilephonelist;
	public String positiveNamedEntity;
	public String negative;
	public String negativeNamedEntity;
	public String trainingSet1;
	public String trainingSet2;
	public String trainingSentence;
	public String posTagger;
	public String modifiedBrownCluster;
	public String trainingdata;
	public String modifiedOfficialName;
	
	public static synchronized Property getInstance() {
		if (property == null) {
			property = new Property ();
		}
		return property;
	}
	
	private void buildDictionary(String path){ //generate directory if it does not exist
		if(path.endsWith("/")){
			File file = new File(path);
			if(!file.exists()){
				file.mkdirs();
			}
			
		}
		if(path.endsWith(".txt")){
			String[] splits = path.split("/");
			StringBuffer sb = new StringBuffer();
			for(int i =0;i<splits.length-1;i++){
				sb.append(splits[i]+"/");
			}
			File file = new File(sb.toString());
			if(!file.exists()){
				file.mkdirs();
			}
		}
	}
	
	private Property(){
		try{
			Properties property = new Properties();
			property.load(new FileReader("config.properties"));
			engineerPath = property.getProperty("engineerPath");
			forumData = property.getProperty("forumData");
			officialname = property.getProperty("officialname");
			brownCluster = property.getProperty("brownCluster");
			brandCluster = property.getProperty("brandCluster");
			nameCluster = property.getProperty("nameCluster");
			brandPath = property.getProperty("brandPath");
			preprocessDoc = property.getProperty("preprocessDoc");
			originalDoc = property.getProperty("originalDoc");
			candidateName = property.getProperty("candidateName");
			stoplist = property.getProperty("stoplist");
			userFrequency = Integer.valueOf(property.getProperty("userFrequency"));
			candidateNameStep1 = property.getProperty("candidateNameStep1");
			candidateNameStep2Pre = property.getProperty("candidateNameStep2Pre");
			candidateNameStep2 = property.getProperty("candidateNameStep2");
			namedEntity = property.getProperty("namedEntity");
			modifiedSentence = property.getProperty("modifiedSentence");
			modifiedSearchEngineer = property.getProperty("modifiedSearchEngineer");
			modifiedSearchEngineerTitle = property.getProperty("modifiedSearchEngineerTitle");
			confidenceValue = property.getProperty("confidenceValue");
			usefulNamedEntity = property.getProperty("usefulNamedEntity");
			extendedUsedfulNamedEntity = property.getProperty("extendedUsedfulNamedEntity");
			mobilephonelist1 = property.getProperty("mobilephonelist1");
			mobilephonelist2 = property.getProperty("mobilephonelist2");
			absoluteConfidenceValue = property.getProperty("absoluteConfidenceValue");
			mobilephonelist = property.getProperty("mobilephonelist");
			positiveNamedEntity = property.getProperty("positiveNamedEntity");
			negative = property.getProperty("negative");
			negativeNamedEntity = property.getProperty("negativeNamedEntity");
			trainingSet1 = property.getProperty("trainingSet1");
			trainingSet2 = property.getProperty("trainingSet2");
			trainingSentence = property.getProperty("trainingSentence");
			posTagger = property.getProperty("posTagger");
			modifiedBrownCluster = property.getProperty("modifiedBrownCluster");
			trainingdata = property.getProperty("trainingdata");
			modifiedOfficialName= property.getProperty("modifiedOfficialName");
			
			buildDictionary(engineerPath);	
			buildDictionary(brownCluster);
			buildDictionary(brandCluster);
			buildDictionary(nameCluster);
			buildDictionary(brandPath);	
			buildDictionary(preprocessDoc);
			buildDictionary(originalDoc);
			buildDictionary(candidateName);	
			buildDictionary(candidateNameStep1);
			buildDictionary(candidateNameStep2Pre);	
			buildDictionary(candidateNameStep2);
			buildDictionary(namedEntity);		
			buildDictionary(modifiedSentence);
			buildDictionary(modifiedSearchEngineer);
			buildDictionary(modifiedSearchEngineerTitle);		
			buildDictionary(confidenceValue);
			buildDictionary(usefulNamedEntity);		
			buildDictionary(extendedUsedfulNamedEntity);
			buildDictionary(mobilephonelist1);
			buildDictionary(mobilephonelist2);
			buildDictionary(absoluteConfidenceValue);
			buildDictionary(mobilephonelist);
			buildDictionary(positiveNamedEntity);
			buildDictionary(negativeNamedEntity);
			buildDictionary(trainingSet1);
			buildDictionary(trainingSet2);
			buildDictionary(trainingSentence);
			buildDictionary(modifiedBrownCluster);
			buildDictionary(trainingdata);
			buildDictionary(modifiedOfficialName);
			
		}catch(Exception e){
			e.printStackTrace();
		}
	}
}

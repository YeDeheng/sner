package crfTrainingData;

public class MainControlforTraningDataGeneration {
	public static void main(String[] args){
		/*
		 * each step can be conducted separately
		 */
//		NegativeNamedEntity negativeNamedEntity = new NegativeNamedEntity(); //format negative named entities
//		negativeNamedEntity.initial();
//		System.out.println("step1");
//		
//		PositiveNamedEntity positiveNamedEntity = new PositiveNamedEntity(); //obtain and format positive named entities
//		positiveNamedEntity.initial();
//		System.out.println("step2");
//		
//		TrainingSentence trainingSentence = new TrainingSentence(); //obtain the training sentences
//		trainingSentence.control();
//		System.out.println("step3");
		
		Feature feature = new Feature(); //assign features to each word in sentences
		feature.control();
		System.out.println("step4");
	}
}

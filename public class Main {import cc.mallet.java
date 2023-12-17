public class Main {import cc.mallet.pipe.*;
    import cc.mallet.pipe.iterator.*;
    import cc.mallet.topics.*;
    import cc.mallet.types.*;
    import java.io.*;
    import java.util.*;
    import java.util.regex.*;
    
    public class AnaliseTextual {
    
        public static void main(String[] args) throws Exception {
            // Pipes: lowercase, tokenize, remove stopwords, map to features
            ArrayList<Pipe> pipeList = new ArrayList<Pipe>();
            pipeList.add(new CharSequenceLowercase());
            pipeList.add(new CharSequence2TokenSequence(Pattern.compile("\\p{L}[\\p{L}\\p{P}]+\\p{L}")));
            pipeList.add(new TokenSequenceRemoveStopwords(new File("stoplists/pt.txt"), "UTF-8", false, false, false));
            pipeList.add(new TokenSequence2FeatureSequence());
    
            // InstanceList para armazenar as instâncias
            InstanceList instances = new InstanceList(new SerialPipes(pipeList));
    
            // Directory contendo os textos
            File directory = new File("exemplos");
            File[] files = directory.listFiles((dir, name) -> name.endsWith(".txt"));
            
            if (files != null) {
                for (File file : files) {
                    // Ler e processar cada arquivo de texto no diretório
                    Reader fileReader = new InputStreamReader(new FileInputStream(file), "UTF-8");
                    instances.addThruPipe(new CsvIterator(fileReader, Pattern.compile("^(.*)$"), 1, -1, -1)); // assumindo um documento por linha
                }
            }
    
            // O resto do seu código existente para criar e estimar o modelo LDA...
            int numTopics = 3;
            ParallelTopicModel model = new ParallelTopicModel(numTopics);
            model.addInstances(instances);
            model.setNumThreads(2);
            model.setNumIterations(1000);
            model.estimate();
    
            // Imprimir as palavras-chave para cada tópico...
            Object[][] topicWords = model.getTopWords(10);
            for (int topic = 0; topic < numTopics; topic++) {
                System.out.println("Tópico " + topic + ":");
                for (int word = 0; word < 10; word++) {
                    System.out.print((String) topicWords[topic][word] + "  ");
                }
                System.out.println();
            }
        }
    }
    
    
}

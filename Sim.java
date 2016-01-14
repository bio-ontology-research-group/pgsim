import java.io.*;
import java.util.*;
import java.util.logging.*;
import java.util.function.IntToDoubleFunction;

import org.openrdf.model.URI;
import slib.graph.algo.utils.GAction;
import slib.graph.algo.utils.GActionType;
import slib.graph.algo.utils.GraphActionExecutor;
import slib.graph.io.conf.GDataConf;
import slib.graph.io.loader.GraphLoaderGeneric;
import slib.graph.io.util.GFormat;
import slib.graph.model.graph.G;
//import org.openrdf.model.vocabulary.RDFS;
import slib.graph.model.impl.graph.memory.GraphMemory;
import slib.graph.model.impl.repo.URIFactoryMemory;
import slib.graph.model.repo.URIFactory;
import slib.graph.algo.accessor.GraphAccessor;
import slib.sml.sm.core.engine.SM_Engine;
import slib.sml.sm.core.metrics.ic.utils.IC_Conf_Topo;
import slib.sml.sm.core.metrics.ic.utils.ICconf;
import slib.sml.sm.core.utils.SMConstants;
import slib.sml.sm.core.utils.SMconf;
import slib.utils.ex.SLIB_Exception;

import slib.utils.ex.SLIB_Ex_Critic;

public class Sim {

  URIFactory uriFactory;
  G graph;
  Gene[] genes;

  public Sim() throws SLIB_Exception {
    this.uriFactory = URIFactoryMemory.getSingleton();
    graph = this.getGeneOntology();
    genes = this.getGenes();
  }

  public G getGeneOntology() throws SLIB_Exception {
    // 1. CREATE GO ONTOLOGY
    // Access to the in-memory URI Factory.
    URIFactory factory = this.uriFactory;

    URI graph_uri = factory.getURI("http://go/");
    factory.loadNamespacePrefix("GO", graph_uri.toString());
    G graph = new GraphMemory(graph_uri);

    // Load OBO file to graph "gene_ontology_ext.obo"
    GDataConf goConf = new GDataConf(GFormat.OBO, "data/gene_ontology_ext.obo");
    GraphLoaderGeneric.populate(goConf, graph);

    // Add virtual root for 3 subontologies__________________________________
    URI virtualRoot = factory.getURI("http://go/virtualRoot");
    graph.addV(virtualRoot);
    GAction rooting = new GAction(GActionType.REROOTING);
    rooting.addParameter("root_uri", virtualRoot.stringValue());
    GraphActionExecutor.applyAction(factory, rooting, graph);
    return graph;
  }

  public Gene[] getGenes() {
    // 2. ANNOTATE 5000 GENE PRODUCTS FROM ANNOTATION FILE
    int geneNum = 5000;
    int annotSizesNum = 5;
    int gN_div_aN = geneNum / annotSizesNum;
    Gene[] genes = new Gene[geneNum];
    for (int i = 0; i < geneNum; i++) {
      genes[i] = new Gene(i + 1, new LinkedHashSet());
    }

    FileInputStream fis = null;
    BufferedReader reader = null;
    try {
      fis = new FileInputStream("data/annotations_plain.txt");
      reader = new BufferedReader(new InputStreamReader(fis));
      String line;

      //i) 1000 gene products with annotation size 1
      for (int i = 0; i < gN_div_aN; i++) {
        line = reader.readLine();
        genes[i].addAnnotation(this.uriFactory.getURI(line));
      }

      //ii) 1000 gene products with annotation size 10
      for (int i = gN_div_aN; i < 2 * gN_div_aN; i++) {
        for (int j = 0; j < 10; j++) {
          line = reader.readLine();
          genes[i].addAnnotation(this.uriFactory.getURI(line));
        }
      }

      //iii) 1000 gene products with annotation size 50
      for (int i = 2*gN_div_aN; i < 3 * gN_div_aN; i++) {
        for (int j = 0; j < 50; j++) {
          line = reader.readLine();
          genes[i].addAnnotation(this.uriFactory.getURI(line));
        }
      }

      //iv) 1000 gene products with annotation size 100
      for (int i = 3*gN_div_aN; i < 4 * gN_div_aN; i++) {
        for (int j = 0; j < 100; j++) {
          line = reader.readLine();
          genes[i].addAnnotation(this.uriFactory.getURI(line));
        }
      }

      //v) 1000 gene products with annotation size 1000
      for (int i = 4 * gN_div_aN; i < geneNum; i++) {
        for (int j = 0; j < 1000; j++) {
          line = reader.readLine();
          genes[i].addAnnotation(this.uriFactory.getURI(line));
        }
      }
    } catch (FileNotFoundException ex) {
      Logger.getLogger(Sim.class.getName()).log(Level.SEVERE, null, ex);
    } catch (IOException ex) {
      Logger.getLogger(Sim.class.getName()).log(Level.SEVERE, null, ex);
    } finally {
      try {
        reader.close();
        fis.close();
      } catch (IOException ex) {
        Logger.getLogger(Sim.class.getName()).log(Level.SEVERE, null, ex);
      }
    }
    return genes;
  }

  public void runGroupwiseMeasures() throws SLIB_Exception {
    final int geneNum = genes.length;

    // // Vertices excluding gene products______________________________________
    // Set<URI> vertices = GraphAccessor.getClasses(graph);

    // 3. CREATE SETS OF ALL POSSIBLE PAIR AND GROUP MEASURES
    final SM_Engine engine = new SM_Engine(this.graph);
    final ICconf icConf = new IC_Conf_Topo("Resnik", SMConstants.FLAG_ICI_RESNIK_1995);
    final Sim that = this;
    for (String flag: SMConstants.SIM_GROUPWISE_DAG.keySet()) {
      final SMconf smConf = new SMconf(flag);
      smConf.setICconf(icConf);

      // 4. CALCULATE ALL MEASURES
      double[] similarities = new double[geneNum * geneNum];
      // Direct groupwise similarity in parallel.
      IntToDoubleFunction compare = new IntToDoubleFunction() {
        @Override
        public double applyAsDouble(int i) {
          try {
            return engine.compare(
              smConf,
              that.genes[i / geneNum].getAnnotations(),
              that.genes[i % geneNum].getAnnotations());
          } catch (SLIB_Ex_Critic ex) {
            Logger.getLogger(Sim.class.getName()).log(Level.SEVERE, null, ex);
          }
          return -2.0;
        }
      };
      Arrays.parallelSetAll(similarities, compare);
      this.saveResults(flag, similarities);
    }
  }

  public void runPairwiseMeasures() throws SLIB_Exception {
    final int geneNum = genes.length;

    // // Vertices excluding gene products______________________________________
    // Set<URI> vertices = GraphAccessor.getClasses(graph);

    // 3. CREATE SETS OF ALL POSSIBLE PAIR AND GROUP MEASURES
    final SM_Engine engine = new SM_Engine(this.graph);
    String[] flags = new String[] {
      SMConstants.FLAG_SIM_GROUPWISE_BMA,
      SMConstants.FLAG_SIM_GROUPWISE_BMM,
      SMConstants.FLAG_SIM_GROUPWISE_MAX,
      SMConstants.FLAG_SIM_GROUPWISE_MIN,
      SMConstants.FLAG_SIM_GROUPWISE_MAX_NORMALIZED_GOSIM
    };
    final ICconf icConf = new IC_Conf_Topo("Resnik", SMConstants.FLAG_ICI_RESNIK_1995);
    final Sim that = this;
    for (String flagGroupwise: flags) {
      final SMconf smConfGroupwise = new SMconf(flagGroupwise);
      for (String flagPairwise: SMConstants.PAIRWISE_MEASURE_FLAGS) {

        final SMconf smConfPairwise = new SMconf(flagPairwise);
        smConfPairwise.setICconf(icConf);
        // Schlicker indirect
        if (flagPairwise.equals(SMConstants.FLAG_SIM_PAIRWISE_DAG_NODE_SCHLICKER_2006)) {
          ICconf prob = new IC_Conf_Topo(SMConstants.FLAG_ICI_PROB_OCCURENCE_PROPAGATED);
          smConfPairwise.addParam("ic_prob", prob);
        }
        // 4. CALCULATE ALL MEASURES
        double[] similarities = new double[geneNum * geneNum];
        // Direct groupwise similarity in parallel.
        IntToDoubleFunction compare = new IntToDoubleFunction() {
          @Override
          public double applyAsDouble(int i) {
            try {
              return engine.compare(
                smConfGroupwise,
                smConfPairwise,
                that.genes[i / geneNum].getAnnotations(),
                that.genes[i % geneNum].getAnnotations());
            } catch (SLIB_Ex_Critic ex) {
              Logger.getLogger(Sim.class.getName()).log(Level.SEVERE, null, ex);
            }
            return -2.0;
          }
        };
        Arrays.parallelSetAll(similarities, compare);
        this.saveResults(flagGroupwise + "__" + flagPairwise, similarities);
      }
    }
  }

  public void saveResults(String filename, double[] similarities) {
    try {
      OutputStream os = new FileOutputStream(filename + ".bin");
      DataOutputStream dos = new DataOutputStream(os);
      for (int i = 0; i < similarities.length; i++) {
        dos.writeDouble(similarities[i]);
      }
      dos.close();
    } catch (IOException ex) {
      Logger.getLogger(Sim.class.getName()).log(Level.SEVERE, null, ex);
    }
  }

  public static void main(String[] args) throws SLIB_Exception {
    new Sim().runGroupwiseMeasures();
    // for (String key: SMConstants.SIM_GROUPWISE_DAG.keySet()) {
    //   System.out.println(key + " " + SMConstants.SIM_GROUPWISE_DAG.get(key));
    // }
  }

  class Gene {

    public int id;
    public Set<URI> annotations;

    public Gene(int id, Set<URI> annotations) {
      this.id  = id;
      this.annotations = annotations;
    }

    public void addAnnotation(URI annotation) {
      this.annotations.add(annotation);
    }

    public Set<URI> getAnnotations() {
      return this.annotations;
    }

  }

}


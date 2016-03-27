@Grab(group='com.github.sharispe', module='slib-sml', version='0.9.1')
@Grab(group='org.codehaus.gpars', module='gpars', version='1.1.0')

import java.net.*
import org.openrdf.model.vocabulary.*
import slib.sglib.io.loader.*
import slib.sml.sm.core.metrics.ic.utils.*
import slib.sml.sm.core.utils.*
import slib.sglib.io.loader.bio.obo.*
import org.openrdf.model.URI
import slib.graph.algo.extraction.rvf.instances.*
import slib.sglib.algo.graph.utils.*
import slib.utils.impl.Timer
import slib.graph.algo.extraction.utils.*
import slib.graph.model.graph.*
import slib.graph.model.repo.*
import slib.graph.model.impl.graph.memory.*
import slib.sml.sm.core.engine.*
import slib.graph.io.conf.*
import slib.graph.model.impl.graph.elements.*
import slib.graph.algo.extraction.rvf.instances.impl.*
import slib.graph.model.impl.repo.*
import slib.graph.io.util.*
import slib.graph.io.loader.*
import groovyx.gpars.GParsPool



def factory = URIFactoryMemory.getSingleton()

class Gene {

  int id
  Set annotations

  public Gene(id, annotations) {
    setId(id)
    setAnnotations(annotations)
  }

  void addAnnotation(annotation) {
    annotations.add(annotation);
  }

  def getAnnotations() {
    annotations
  }

}


def getGeneOntology = {

  URI graph_uri = factory.getURI("http://go/")
  factory.loadNamespacePrefix("GO", graph_uri.toString())
  G graph = new GraphMemory(graph_uri)

  // Load OBO file to graph "gene_ontology_ext.obo"
  GDataConf goConf = new GDataConf(GFormat.OBO, "data/gene_ontology_ext.obo")
  GraphLoaderGeneric.populate(goConf, graph)

  // Add virtual root for 3 subontologies__________________________________
  URI virtualRoot = factory.getURI("http://go/virtualRoot")
  graph.addV(virtualRoot)
  GAction rooting = new GAction(GActionType.REROOTING)
  rooting.addParameter("root_uri", virtualRoot.stringValue())
  GraphActionExecutor.applyAction(factory, rooting, graph)
  return graph
}

def getGenes = {
  def geneNum = 1000
  def geneGroups = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  def genes = new Gene[geneNum]
  new File("data/annotations_plain.txt").eachLine { line, i ->
    i -= 1
    def s = 0
    for (def j = 0; j < geneGroups.size(); j++) {
        def g = geneGroups[j]
        s += g * 100
        if (i < s) {
            def id = (i - (s - g * 100)).intdiv(g) + j * 100
            if (genes[id] == null) genes[id] = new Gene(id, new LinkedHashSet())
            genes[id].addAnnotation(factory.getURI(line))
            break
        }
    }

  }
  return genes
}

graph = getGeneOntology()
genes = getGenes()

def sim_id = this.args[0].toInteger()

SM_Engine engine = new SM_Engine(graph)

// BMA+Resnik, BMA+Schlicker2006, BMA+Lin1998, BMA+Jiang+Conrath1997,
// DAG-GIC, DAG-NTO, DAG-UI

String[] flags = [
  SMConstants.FLAG_SIM_GROUPWISE_BMA,
//  SMConstants.FLAG_SIM_GROUPWISE_BMM,
//  SMConstants.FLAG_SIM_GROUPWISE_MAX,
//  SMConstants.FLAG_SIM_GROUPWISE_MIN,
//  SMConstants.FLAG_SIM_GROUPWISE_MAX_NORMALIZED_GOSIM
]
// List<String> pairFlags = new ArrayList<String>(SMConstants.PAIRWISE_MEASURE_FLAGS);
String[] pairFlags = [
  SMConstants.FLAG_SIM_PAIRWISE_DAG_EDGE_RESNIK_1995,
  SMConstants.FLAG_SIM_PAIRWISE_DAG_NODE_RESNIK_1995,
  SMConstants.FLAG_SIM_PAIRWISE_DAG_NODE_SCHLICKER_2006,
  SMConstants.FLAG_SIM_PAIRWISE_DAG_NODE_LIN_1998,
  SMConstants.FLAG_SIM_PAIRWISE_DAG_NODE_JIANG_CONRATH_1997_NORM
]

ICconf icConf = new IC_Conf_Topo("Resnik", SMConstants.FLAG_ICI_RESNIK_1995);
String flagGroupwise = flags[sim_id.intdiv(5)];
String flagPairwise = pairFlags[sim_id % 5];
SMconf smConfGroupwise = new SMconf(flagGroupwise);
SMconf smConfPairwise = new SMconf(flagPairwise);
smConfPairwise.setICconf(icConf);

// Schlicker indirect
ICconf prob = new IC_Conf_Topo(SMConstants.FLAG_ICI_PROB_OCCURENCE_PROPAGATED);
smConfPairwise.addParam("ic_prob", prob);

def result = new Double[1000000]
for (i = 0; i < 1000000; i++) {
  result[i] = i
}

def c = 0

GParsPool.withPool {
  result.eachParallel { val ->
    def i = val.toInteger()
    def x = i.intdiv(1000)
    def y = i % 1000
    if (x <= y) {
      result[i] = engine.compare(
              smConfGroupwise,
              smConfPairwise,
              genes[x].getAnnotations(),
              genes[y].getAnnotations())
      println c
      c++
    }
  }
}

def fout = new PrintWriter(new BufferedWriter(
  new FileWriter(flagGroupwise + "_" + flagPairwise + ".txt")))
for (i = 0; i < 1000000; i++) {
  def x = i.intdiv(1000)
  def y = i % 1000
  if (x <= y) {
    fout.println(result[i])
  } else {
    def j = y * 1000 + x
    fout.println(result[j])
  }
}
fout.flush()
fout.close()

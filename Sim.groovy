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
  def geneNum = 5000
  def genes = new Gene[geneNum]
  new File("data/annotations_plain.txt").eachLine { line, i ->
    i -= 1
    if (i < 1000) {
      genes[i] = new Gene(i, new LinkedHashSet())
      genes[i].addAnnotation(factory.getURI(line))
    } else if (i < 11000) {
      def id = (i - 1000).intdiv(10) + 1000
      if (genes[id] == null) genes[id] = new Gene(id, new LinkedHashSet())
      genes[id].addAnnotation(factory.getURI(line))
    } else if (i < 61000) {
      def id = (i - 11000).intdiv(50) + 2000
      if (genes[id] == null) genes[id] = new Gene(id, new LinkedHashSet())
      genes[id].addAnnotation(factory.getURI(line))
    } else if (i < 161000) {
      def id = (i - 61000).intdiv(100) + 3000
      if (genes[id] == null) genes[id] = new Gene(id, new LinkedHashSet())
      genes[id].addAnnotation(factory.getURI(line))
    } else {
      def id = (i - 161000).intdiv(1000) + 4000
      if (genes[id] == null) genes[id] = new Gene(id, new LinkedHashSet())
      genes[id].addAnnotation(factory.getURI(line))

    }
  }
  return genes
}

graph = getGeneOntology()
genes = getGenes()

def sim_id = this.args[0].toInteger()

SM_Engine engine = new SM_Engine(graph)

String[] flags = [
  SMConstants.FLAG_SIM_GROUPWISE_BMA,
  SMConstants.FLAG_SIM_GROUPWISE_BMM,
  SMConstants.FLAG_SIM_GROUPWISE_MAX,
  SMConstants.FLAG_SIM_GROUPWISE_MIN,
  SMConstants.FLAG_SIM_GROUPWISE_MAX_NORMALIZED_GOSIM
]
List<String> pairFlags = new ArrayList<String>(SMConstants.PAIRWISE_MEASURE_FLAGS);

ICconf icConf = new IC_Conf_Topo("Resnik", SMConstants.FLAG_ICI_RESNIK_1995);
String flagGroupwise = flags[sim_id.intdiv(38)];
String flagPairwise = pairFlags.get(sim_id % 38);
SMconf smConfGroupwise = new SMconf(flagGroupwise);
SMconf smConfPairwise = new SMconf(flagPairwise);
smConfPairwise.setICconf(icConf);

// Schlicker indirect
ICconf prob = new IC_Conf_Topo(SMConstants.FLAG_ICI_PROB_OCCURENCE_PROPAGATED);
smConfPairwise.addParam("ic_prob", prob);

def result = new Double[25000000]
for (i = 0; i < 25000000; i++) {
  result[i] = i
}

def c = 0

GParsPool.withPool {
  result.eachParallel { val ->
    def i = val.toInteger()
    def x = i.intdiv(5000)
    def y = i % 5000
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
  new FileWriter(this.args[0] + "_" + flagGroupwise + "_" + flagPairwise + ".txt")))
for (i = 0; i < 25000000; i++) {
  def x = i.intdiv(5000)
  def y = i % 5000
  if (x <= y) {
    fout.println(result[i])
  } else {
    def j = y * 5000 + x
    fout.println(result[j])
  }
}
fout.flush()
fout.close()

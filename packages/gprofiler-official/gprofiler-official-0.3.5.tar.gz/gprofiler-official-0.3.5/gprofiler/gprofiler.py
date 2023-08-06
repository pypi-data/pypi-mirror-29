
import pprint
import re
import urllib.request, urllib.parse, urllib.error

from . import paramtransform

class GProfiler:
    
    """
    A class representing the g:Profiler toolkit. Contains methods for
    querying the g:GOSt, g:Convert and g:Orth tools. Please see the
    g:Profiler_ web tool for extensive documentation on all the options to
    the methods.
    
    * ``user_agent`` - **Required** (*String*) A short user agent string for
      your tool.
    * ``base_url`` - (*String*) An absolute URL of the g:Profiler instance
      to use; the stable release by default.
    * ``output_type`` - Controls the data structure returned from the methods.
    
      - ``GProfiler.OUTPUT_TYPE_FORMATTED`` - **Default** Returns a list
        (lines) of lists (fields), with each field cast into its proper type
        or ``None`` for "N/A" values.
      - ``GProfiler.OUTPUT_TYPE_LINES`` - Returns a list containing the raw
        lines from g:Profiler.
    * ``want_header`` - Prepend the header (column names) as the first row
      of output; false by default.
        
    Options common to several methods:
    
    * ``query`` - **Required** (*String* | *List*) The query is a space-
      separated string or a list of genes, proteins or other
      biological entities.
    * ``organism`` - (*String*) The organism name in g:Profiler format. The
      full list of organisms is available `here
      <http://biit.cs.ut.ee/gprofiler/help.cgi?help_id=64>`_.
    * ``region_query`` - (*Boolean*) The query consists of
      chromosomal regions.
    * ``numeric_ns`` - (*String*) Namespace to use for fully numeric IDs.
    
    .. _g:Profiler: http://biit.cs.ut.ee/gprofiler
    """
    
    _DEFAULT_BASE_URL = "http://biit.cs.ut.ee/gprofiler/"

    DOMAIN_ANNOTATED = 1
    DOMAIN_KNOWN = 2
    
    HIERF_MODERATE = 5
    HIERF_STRONG = 6

    OUTPUT_TYPE_FORMATTED = 10
    OUTPUT_TYPE_LINES = 11
    
    THR_GSCS = 15
    THR_FDR = 16
    THR_BONFERRONI = 17

    def __init__(
        self, user_agent, 
        base_url=_DEFAULT_BASE_URL, output_type=OUTPUT_TYPE_FORMATTED,
        want_header=False
    ):
        self.base_url = self._DEFAULT_BASE_URL if (not base_url) else base_url
        self.user_agent = user_agent
        self.output_type = output_type
        self.want_header = want_header
        self.paramtransformer = paramtransform.ParamTransformer()

    def gprofile(self, query,
        organism            = "hsapiens",
        all_results         = False,
        ordered             = False,
        region_query        = False,
        exclude_iea         = False,
        underrep            = False,
        evcodes             = False,
        hier_sorting        = False,
        hier_filtering      = None,
        max_p_value         = 1.0,
        min_set_size        = None,
        max_set_size        = None,
        min_isect_size      = None,
        max_isect_size      = None,
        correction_method   = None,
        domain_size         = None,
        numeric_ns          = None,
        custom_bg           = None,
        src_filter          = None
    ):
        
        """
        Query g:GOSt.
        
        * ``all_results`` - (*Boolean*) All results, including those deemed not
          significant.
        * ``ordered`` - (*Boolean*) Ordered query.
        * ``exclude_iea`` - (*Boolean*) Exclude electronic GO annotations.
        * ``underrep`` - (*Boolean*) Measure underrepresentation.
        * ``evcodes`` - (*Boolean*) Request evidence codes in output as the
          final column.
        * ``hier_sorting`` - (*Boolean*) Sort output into subgraphs.
        * ``hier_filtering`` - (*Boolean*) Hierarchical filtering.
        * ``max_p_value`` - (*Float*) Custom p-value threshold.
        * ``min_set_size`` - (*Int*) Minimum size of functional category.
        * ``max_set_size`` - (*Int*) Maximum size of functional category.
        * ``min_isect_size`` - (*Int*) Minimum size of query / functional
          category intersection.
        * ``max_isect_size`` - (*Int*) Maximum size of query / functional
          category intersection.
        * ``correction_method`` - Algorithm used for multiple testing
          correction, one of:
          
          - ``GProfiler.THR_GSCS`` **Default** g:SCS.
          - ``GProfiler.THR_FDR`` Benjamini-Hochberg FDR.
          - ``GProfiler.THR_BONFERRONI`` Bonferroni.
          
        * ``domain_size`` - Statistical domain size, one of:
        
          - ``GProfiler.DOMAIN_ANNOTATED`` - **Default** Only annotated genes.
          - ``GProfiler.DOMAIN_KNOWN`` - All known genes.
        
        * ``custom_bg`` - (*String* | *List*) Custom statistical background
        * ``src_filter`` - (*List*) A list of data source ID strings, e.g.
          ``["GO:BP", "KEGG"]``. These currently include GO (GO:BP, GO:MF,
          GO:CC to select a particular GO branch), KEGG, REAC, TF, MI, CORUM,
          HP, HPA, OMIM.
        """
        
        gp_args = locals()
        arg_transformer = self._get_gprofile_postdata
        output_spec = [
            int, bool, float, int, int, int, float,
            float, str, str, int, str, int, str, str
        ]

        return self._invoke_tool("index.cgi", gp_args, arg_transformer, output_spec)

    def gconvert(self, query,
        organism        = "hsapiens",
        target          = "ENSG",
        region_query    = False,
        numeric_ns      = None,
    ):
        
        """
        Query g:Convert.
        
        * ``target`` - (*String*) The target namespace.
        """
        
        gp_args = locals()
        arg_transformer = self._get_gconvert_postdata
        output_spec = [int, str, str, str, str, str, str]
        hdr = "\t".join([
            "g#", "initial alias", "c#", "converted alias", 
            "name", "description", "namespaces"
        ])
        
        return self._invoke_tool("gconvert.cgi", gp_args, arg_transformer, output_spec, hdr)

    def gorth(self, query,
        source_organism = "hsapiens",
        target_organism = "mmusculus",
        region_query    = False,
        numeric_ns      = None,
    ):
        
        """
        Query g:Orth.
        
        * ``source_organism``, ``target_organism`` - The source and target
          organism IDs, in g:Profiler format
        """
        
        gp_args = locals()
        arg_transformer = self._get_gorth_postdata
        output_spec = [int, str, str, str, str, str, str]
        hdr = "\t".join([
            "g#", "initial alias", "initial ENSG", "o#", "ortholog ENSG", 
            "ortholog name", "ortholog description"
        ])

        return self._invoke_tool("gorth.cgi", gp_args, arg_transformer, output_spec, hdr)

    def _get_gprofile_postdata(self, args):
        pt = self.paramtransformer
        postdata = pt.transform(args, {
            "organism"          : "organism",
            "query"             : [pt.TF_LIST, "query"],
            "all_results"       : [pt.TF_BOOL, "significant", True],
            "ordered"           : [pt.TF_BOOL, "ordered_query"],
            "region_query"      : [pt.TF_BOOL, "region_query"],
            "exclude_iea"       : [pt.TF_BOOL, "no_iea"],
            "underrep"          : [pt.TF_BOOL, "underrep"],
            "evcodes"           : [pt.TF_BOOL, "txt_evcodes"],
            "hier_sorting"      : [pt.TF_BOOL, "sort_by_structure"],
            "hier_filtering"    : [pt.TF_MAP, "hierfiltering", {
                GProfiler.HIERF_MODERATE    : "compact_rgroups",
                GProfiler.HIERF_STRONG      : "compact_ccomp"
            }],
            "max_p_value"       : "user_thr",
            "min_set_size"      : "min_set_size",
            "max_set_size"      : "max_set_size",
            "min_isect_size"    : "min_isect_size",
            "max_isect_size"    : "max_isect_size",
            "correction_method" : [pt.TF_MAP, "threshold_algo", {
                GProfiler.THR_GSCS          : "analytical",
                GProfiler.THR_FDR           : "fdr",
                GProfiler.THR_BONFERRONI    : "bonferroni"
            }],
            "domain_size"       : [pt.TF_MAP, "domain_size_type", {
                GProfiler.DOMAIN_ANNOTATED  : "annotated",
                GProfiler.DOMAIN_KNOWN      : "known"
            }],
            "numeric_ns"        : "prefix",
            "custom_bg"         : [pt.TF_LIST, "custbg"],
            "src_filter"        : [pt.TF_SRCFILTER, None]
        })

        return postdata

    def _get_gconvert_postdata(self, args):
        pt = self.paramtransformer
        postdata = pt.transform(args, {
            "query"         : [pt.TF_LIST, "query"],
            "organism"      : "organism",
            "target"        : "target",
            "numeric_ns"    : "prefix",
            "region_query"  : [pt.TF_BOOL, "region_query"],
        })

        return postdata

    def _get_gorth_postdata(self, args):
        pt = self.paramtransformer
        postdata = pt.transform(args, {
            "query"             : [pt.TF_LIST, "query"],
            "source_organism"   : "organism",
            "target_organism"   : "target",
            "numeric_ns"        : "prefix",
            "region_query"      : [pt.TF_BOOL, "region_query"],
        })

        return postdata

    def _invoke_tool(self, tool_url, tool_args, arg_transformer, output_spec, header=None):
        postdata = \
            arg_transformer(tool_args)
        http_result = \
            self._make_http_request(tool_url, postdata)
        return self._format_output(http_result, output_spec, header)

    def _make_http_request(self, tool_url, postdata):
        postdata.update({
            "output" : "mini"
        })

        full_url = self.base_url + "/" + tool_url
        data = urllib.parse.urlencode(postdata).encode("ascii")
        headers = { "User-Agent" : self.user_agent }
        rq = urllib.request.Request(full_url, data, headers)

        return urllib.request.urlopen(rq, timeout=60*30)

    def _format_output(self, http_res, output_spec, header):

        """ Format raw output from the service according to output_spec and
        self.output_type. If header requested: add the explicit header string
        passed as an argument; otherwise consider first row returned from the
        service to be the header.
        """

        result = []
        
        def append_line(result, line, is_hdr):
            if (self.output_type == self.OUTPUT_TYPE_FORMATTED):
                line = self._format_output_line(line, output_spec, is_hdr)
            result.append(line)
        
        if (self.want_header and header):
            append_line(result, header, True)        

        for (i, line) in enumerate(http_res):
            r = None
            is_hdr = False
            line = str(line, "utf-8")
            
            if (i == 0 and self.want_header and not header and re.search(r"\t", line)):
                is_hdr = True
            elif (re.match(r"\s*#", line)):
                continue
            append_line(result, line, is_hdr)

        return result
    
    def _format_output_line(self, line, output_spec, ignore_types):
        
        """ Format one line of output according to output_spec. If
        ignore_types is true, do not attempt type conversions (useful for the
        header line).
        """
        
        r = []
        fields = [s.strip() for s in line.strip().split("\t")]
        
        if (ignore_types):
            return fields
        
        for i in range(0, len(fields)):
            outtype = output_spec[i]
            value = fields[i]

            if ((outtype is str) and (value == "N/A")): # N/A becomes None
                r.append(None)
            else:
                r.append(outtype(value))
        
        return r

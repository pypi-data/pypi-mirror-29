Configurable Settings
++++++++++++++++++++++++++++++++++++++++++++++++++

.. glossary::
    :sorted:


    aligner
        :class:`~mavis.align.SUPPORTED_ALIGNER` - The aligner to use to map the contigs/reads back to the reference e.g blat or bwa. The corresponding environment variable is ``MAVIS_ALIGNER`` and the default value is ``'blat'``. Accepted values include: ``'bwa mem'``, ``'blat'``

    annotation_filters
        :class:`str` - A comma separated list of filters to apply to putative annotations. The corresponding environment variable is ``MAVIS_ANNOTATION_FILTERS`` and the default value is ``'choose_more_annotated,choose_transcripts_by_priority'``

    annotation_memory
        :class:`int` - Default memory limit (mb) for the annotation stage. The corresponding environment variable is ``MAVIS_ANNOTATION_MEMORY`` and the default value is ``12000``

    assembly_include_flanking_pairs
        :class:`bool` - If true then when the split reads are assembled, any flanking read pairs will also be added. The corresponding environment variable is ``MAVIS_ASSEMBLY_INCLUDE_FLANKING_PAIRS`` and the default value is ``True``

    assembly_include_half_mapped_reads
        :class:`bool` - If true then when the split reads are assembled, any half-mapped read mates will also be added. The corresponding environment variable is ``MAVIS_ASSEMBLY_INCLUDE_HALF_MAPPED_READS`` and the default value is ``True``

    assembly_max_kmer_size
        :class:`int` - The minimum between this and the smallest length input sequence is used as the kmer size for assembling the debruijn graph. if this is not set (any value less than 0 is considered not set) the default is the 75%% of the minimum length input sequence. The corresponding environment variable is ``MAVIS_ASSEMBLY_MAX_KMER_SIZE`` and the default value is ``-1``

    assembly_max_kmer_strict
        :class:`bool` - If true then any sequences input to the assembly algorithm that cannot create a kmer of this size will be discarded. if false, then the kmer size will be reduced to the minimum input and all input sequences will be used in the assembly algorithm. The corresponding environment variable is ``MAVIS_ASSEMBLY_MAX_KMER_STRICT`` and the default value is ``True``

    assembly_max_paths
        :class:`int` - The maximum number of paths to resolve. this is used to limit when there is a messy assembly graph to resolve. the assembly will pre-calculate the number of paths (or putative assemblies) and stop if it is greater than the given setting. The corresponding environment variable is ``MAVIS_ASSEMBLY_MAX_PATHS`` and the default value is ``8``

    assembly_min_edge_weight
        :class:`int` - Discards all edges with a weight/frequency less than this from the debruijn graph. The corresponding environment variable is ``MAVIS_ASSEMBLY_MIN_EDGE_WEIGHT`` and the default value is ``2``

    assembly_min_exact_match_to_remap
        :class:`int` - The minimum length of exact matches to initiate remapping a read to a contig. The corresponding environment variable is ``MAVIS_ASSEMBLY_MIN_EXACT_MATCH_TO_REMAP`` and the default value is ``15``

    assembly_min_nc_edge_weight
        :class:`int` - Discards all non-cutting edges with a weight/frequency less than this from the debruijn graph. The corresponding environment variable is ``MAVIS_ASSEMBLY_MIN_NC_EDGE_WEIGHT`` and the default value is ``3``

    assembly_min_remap_coverage
        :class:`~mavis.constants.float_fraction` - Minimum fraction of the contig sequence which the remapped sequences must align over. The corresponding environment variable is ``MAVIS_ASSEMBLY_MIN_REMAP_COVERAGE`` and the default value is ``0.9``

    assembly_min_remapped_seq
        :class:`int` - The minimum input sequences that must remap for an assembled contig to be used. The corresponding environment variable is ``MAVIS_ASSEMBLY_MIN_REMAPPED_SEQ`` and the default value is ``3``

    assembly_min_tgt_to_exclude_half_map
        :class:`int` - The minimum number of split reads aligning to both breakpoints in order to exclude half-mapped reads from the assembly input. The corresponding environment variable is ``MAVIS_ASSEMBLY_MIN_TGT_TO_EXCLUDE_HALF_MAP`` and the default value is ``7``

    assembly_min_uniq
        :class:`~mavis.constants.float_fraction` - Minimum percent uniq required to keep separate assembled contigs. if contigs are more similar then the lower scoring, then shorter, contig is dropped. The corresponding environment variable is ``MAVIS_ASSEMBLY_MIN_UNIQ`` and the default value is ``0.1``

    assembly_strand_concordance
        :class:`~mavis.constants.float_fraction` - When the number of remapped reads from each strand are compared, the ratio must be above this number to decide on the strand. The corresponding environment variable is ``MAVIS_ASSEMBLY_STRAND_CONCORDANCE`` and the default value is ``0.51``

    blat_limit_top_aln
        :class:`int` - Number of results to return from blat (ranking based on score). The corresponding environment variable is ``MAVIS_BLAT_LIMIT_TOP_ALN`` and the default value is ``10``

    blat_min_identity
        :class:`~mavis.constants.float_fraction` - The minimum percent identity match required for blat results when aligning contigs. The corresponding environment variable is ``MAVIS_BLAT_MIN_IDENTITY`` and the default value is ``0.9``

    breakpoint_color
        :class:`str` - Breakpoint outline color. The corresponding environment variable is ``MAVIS_BREAKPOINT_COLOR`` and the default value is ``'#000000'``

    call_error
        :class:`int` - Buffer zone for the evidence window. The corresponding environment variable is ``MAVIS_CALL_ERROR`` and the default value is ``10``

    clean_aligner_files
        :class:`bool` - Remove the aligner output files after the validation stage is complete. not required for subsequent steps but can be useful in debugging and deep investigation of events. The corresponding environment variable is ``MAVIS_CLEAN_ALIGNER_FILES`` and the default value is ``False``

    cluster_initial_size_limit
        :class:`int` - The maximum cumulative size of both breakpoints for breakpoint pairs to be used in the initial clustering phase (combining based on overlap). The corresponding environment variable is ``MAVIS_CLUSTER_INITIAL_SIZE_LIMIT`` and the default value is ``25``

    cluster_radius
        :class:`int` - Maximum distance allowed between paired breakpoint pairs. The corresponding environment variable is ``MAVIS_CLUSTER_RADIUS`` and the default value is ``100``

    contig_aln_max_event_size
        :class:`int` - Relates to determining breakpoints when pairing contig alignments. for any given read in a putative pair the soft clipping is extended to include any events of greater than this size. the softclipping is added to the side of the alignment as indicated by the breakpoint we are assigning pairs to. The corresponding environment variable is ``MAVIS_CONTIG_ALN_MAX_EVENT_SIZE`` and the default value is ``50``

    contig_aln_merge_inner_anchor
        :class:`int` - The minimum number of consecutive exact match base pairs to not merge events within a contig alignment. The corresponding environment variable is ``MAVIS_CONTIG_ALN_MERGE_INNER_ANCHOR`` and the default value is ``20``

    contig_aln_merge_outer_anchor
        :class:`int` - Minimum consecutively aligned exact matches to anchor an end for merging internal events. The corresponding environment variable is ``MAVIS_CONTIG_ALN_MERGE_OUTER_ANCHOR`` and the default value is ``15``

    contig_aln_min_anchor_size
        :class:`int` - The minimum number of aligned bases for a contig (m or =) in order to simplify. do not have to be consecutive. The corresponding environment variable is ``MAVIS_CONTIG_ALN_MIN_ANCHOR_SIZE`` and the default value is ``50``

    contig_aln_min_extend_overlap
        :class:`int` - Minimum number of bases the query coverage interval must be extended by in order to pair alignments as a single split alignment. The corresponding environment variable is ``MAVIS_CONTIG_ALN_MIN_EXTEND_OVERLAP`` and the default value is ``10``

    contig_aln_min_query_consumption
        :class:`~mavis.constants.float_fraction` - Minimum fraction of the original query sequence that must be used by the read(s) of the alignment. The corresponding environment variable is ``MAVIS_CONTIG_ALN_MIN_QUERY_CONSUMPTION`` and the default value is ``0.9``

    contig_aln_min_score
        :class:`~mavis.constants.float_fraction` - Minimum score for a contig to be used as evidence in a call by contig. The corresponding environment variable is ``MAVIS_CONTIG_ALN_MIN_SCORE`` and the default value is ``0.9``

    contig_call_distance
        :class:`int` - The maximum distance allowed between breakpoint pairs (called by contig) in order for them to pair. The corresponding environment variable is ``MAVIS_CONTIG_CALL_DISTANCE`` and the default value is ``0``

    domain_color
        :class:`str` - Domain fill color. The corresponding environment variable is ``MAVIS_DOMAIN_COLOR`` and the default value is ``'#ccccb3'``

    domain_mismatch_color
        :class:`str` - Domain fill color on 0%% match. The corresponding environment variable is ``MAVIS_DOMAIN_MISMATCH_COLOR`` and the default value is ``'#b2182b'``

    domain_name_regex_filter
        :class:`str` - The regular expression used to select domains to be displayed (filtered by name). The corresponding environment variable is ``MAVIS_DOMAIN_NAME_REGEX_FILTER`` and the default value is ``'^PF\\d+$'``

    domain_scaffold_color
        :class:`str` - The color of the domain scaffold. The corresponding environment variable is ``MAVIS_DOMAIN_SCAFFOLD_COLOR`` and the default value is ``'#000000'``

    draw_fusions_only
        :class:`bool` - Flag to indicate if events which do not produce a fusion transcript should produce illustrations. The corresponding environment variable is ``MAVIS_DRAW_FUSIONS_ONLY`` and the default value is ``True``

    draw_non_synonymous_cdna_only
        :class:`bool` - Flag to indicate if events which are synonymous at the cdna level should produce illustrations. The corresponding environment variable is ``MAVIS_DRAW_NON_SYNONYMOUS_CDNA_ONLY`` and the default value is ``True``

    drawing_width_iter_increase
        :class:`int` - The amount (in  pixels) by which to increase the drawing width upon failure to fit. The corresponding environment variable is ``MAVIS_DRAWING_WIDTH_ITER_INCREASE`` and the default value is ``500``

    fetch_min_bin_size
        :class:`int` - The minimum size of any bin for reading from a bam file. increasing this number will result in smaller bins being merged or less bins being created (depending on the fetch method). The corresponding environment variable is ``MAVIS_FETCH_MIN_BIN_SIZE`` and the default value is ``50``

    fetch_reads_bins
        :class:`int` - Number of bins to split an evidence window into to ensure more even sampling of high coverage regions. The corresponding environment variable is ``MAVIS_FETCH_READS_BINS`` and the default value is ``5``

    fetch_reads_limit
        :class:`int` - Maximum number of reads, cap, to loop over for any given evidence window. The corresponding environment variable is ``MAVIS_FETCH_READS_LIMIT`` and the default value is ``3000``

    filter_cdna_synon
        :class:`bool` - Filter all annotations synonymous at the cdna level. The corresponding environment variable is ``MAVIS_FILTER_CDNA_SYNON`` and the default value is ``True``

    filter_min_flanking_reads
        :class:`int` - Minimum number of flanking pairs for a call by flanking pairs. The corresponding environment variable is ``MAVIS_FILTER_MIN_FLANKING_READS`` and the default value is ``10``

    filter_min_linking_split_reads
        :class:`int` - Minimum number of linking split reads for a call by split reads. The corresponding environment variable is ``MAVIS_FILTER_MIN_LINKING_SPLIT_READS`` and the default value is ``1``

    filter_min_remapped_reads
        :class:`int` - Minimum number of remapped reads for a call by contig. The corresponding environment variable is ``MAVIS_FILTER_MIN_REMAPPED_READS`` and the default value is ``5``

    filter_min_spanning_reads
        :class:`int` - Minimum number of spanning reads for a call by spanning reads. The corresponding environment variable is ``MAVIS_FILTER_MIN_SPANNING_READS`` and the default value is ``5``

    filter_min_split_reads
        :class:`int` - Minimum number of split reads for a call by split reads. The corresponding environment variable is ``MAVIS_FILTER_MIN_SPLIT_READS`` and the default value is ``5``

    filter_protein_synon
        :class:`bool` - Filter all annotations synonymous at the protein level. The corresponding environment variable is ``MAVIS_FILTER_PROTEIN_SYNON`` and the default value is ``True``

    filter_secondary_alignments
        :class:`bool` - Filter secondary alignments when gathering read evidence. The corresponding environment variable is ``MAVIS_FILTER_SECONDARY_ALIGNMENTS`` and the default value is ``True``

    filter_trans_homopolymers
        :class:`bool` - Filter all single bp ins/del/dup events that are in a homopolymer region of at least 5 bps and are not paired to a genomic event. The corresponding environment variable is ``MAVIS_FILTER_TRANS_HOMOPOLYMERS`` and the default value is ``True``

    flanking_call_distance
        :class:`int` - The maximum distance allowed between breakpoint pairs (called by flanking pairs) in order for them to pair. The corresponding environment variable is ``MAVIS_FLANKING_CALL_DISTANCE`` and the default value is ``0``

    fuzzy_mismatch_number
        :class:`int` - The number of events/mismatches allowed to be considered a fuzzy match. The corresponding environment variable is ``MAVIS_FUZZY_MISMATCH_NUMBER`` and the default value is ``1``

    gene1_color
        :class:`str` - The color of genes near the first gene. The corresponding environment variable is ``MAVIS_GENE1_COLOR`` and the default value is ``'#657e91'``

    gene1_color_selected
        :class:`str` - The color of the first gene. The corresponding environment variable is ``MAVIS_GENE1_COLOR_SELECTED`` and the default value is ``'#518dc5'``

    gene2_color
        :class:`str` - The color of genes near the second gene. The corresponding environment variable is ``MAVIS_GENE2_COLOR`` and the default value is ``'#325556'``

    gene2_color_selected
        :class:`str` - The color of the second gene. The corresponding environment variable is ``MAVIS_GENE2_COLOR_SELECTED`` and the default value is ``'#4c9677'``

    import_env
        :class:`bool` - Flag to import environment variables. The corresponding environment variable is ``MAVIS_IMPORT_ENV`` and the default value is ``True``

    input_call_distance
        :class:`int` - The maximum distance allowed between breakpoint pairs (called by input tools, not validated) in order for them to pair. The corresponding environment variable is ``MAVIS_INPUT_CALL_DISTANCE`` and the default value is ``5``

    label_color
        :class:`str` - The label color. The corresponding environment variable is ``MAVIS_LABEL_COLOR`` and the default value is ``'#000000'``

    limit_to_chr
        :class:`~mavis.util.ChrListString` - A semi-colon delimited list of chromosome names to use. breakpointpairs on other chromosomes will be filteredout. for example '1;2;3;4' would filter out events/breakpoint pairs on any chromosomes but 1, 2, 3, and 4. The corresponding environment variable is ``MAVIS_LIMIT_TO_CHR`` and the default value is ``['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', 'X', 'Y']``

    mask_fill
        :class:`str` - Color of mask (for deleted region etc.). The corresponding environment variable is ``MAVIS_MASK_FILL`` and the default value is ``'#ffffff'``

    mask_opacity
        :class:`~mavis.constants.float_fraction` - Opacity of the mask layer. The corresponding environment variable is ``MAVIS_MASK_OPACITY`` and the default value is ``0.7``

    max_drawing_retries
        :class:`int` - The maximum number of retries for attempting a drawing. each iteration the width is extended. if it is still insufficient after this number a gene-level only drawing will be output. The corresponding environment variable is ``MAVIS_MAX_DRAWING_RETRIES`` and the default value is ``5``

    max_files
        :class:`int` - The maximum number of files to output from clustering/splitting. The corresponding environment variable is ``MAVIS_MAX_FILES`` and the default value is ``200``

    max_orf_cap
        :class:`int` - The maximum number of orfs to return (best putative orfs will be retained). The corresponding environment variable is ``MAVIS_MAX_ORF_CAP`` and the default value is ``3``

    max_proximity
        :class:`int` - The maximum distance away from an annotation before the region in considered to be uninformative. The corresponding environment variable is ``MAVIS_MAX_PROXIMITY`` and the default value is ``5000``

    max_sc_preceeding_anchor
        :class:`int` - When remapping a softclipped read this determines the amount of softclipping allowed on the side opposite of where we expect it. for example for a softclipped read on a breakpoint with a left orientation this limits the amount of softclipping that is allowed on the right. if this is set to none then there is no limit on softclipping. The corresponding environment variable is ``MAVIS_MAX_SC_PRECEEDING_ANCHOR`` and the default value is ``6``

    memory_limit
        :class:`int` - The maximum number of megabytes (mb) any given job is allowed. The corresponding environment variable is ``MAVIS_MEMORY_LIMIT`` and the default value is ``16000``

    min_anchor_exact
        :class:`int` - Applies to re-aligning softclipped reads to the opposing breakpoint. the minimum number of consecutive exact matches to anchor a read to initiate targeted realignment. The corresponding environment variable is ``MAVIS_MIN_ANCHOR_EXACT`` and the default value is ``6``

    min_anchor_fuzzy
        :class:`int` - Applies to re-aligning softclipped reads to the opposing breakpoint. the minimum length of a fuzzy match to anchor a read to initiate targeted realignment. The corresponding environment variable is ``MAVIS_MIN_ANCHOR_FUZZY`` and the default value is ``10``

    min_anchor_match
        :class:`~mavis.constants.float_fraction` - Minimum percent match for a read to be kept as evidence. The corresponding environment variable is ``MAVIS_MIN_ANCHOR_MATCH`` and the default value is ``0.9``

    min_clusters_per_file
        :class:`int` - The minimum number of breakpoint pairs to output to a file. The corresponding environment variable is ``MAVIS_MIN_CLUSTERS_PER_FILE`` and the default value is ``50``

    min_domain_mapping_match
        :class:`~mavis.constants.float_fraction` - A number between 0 and 1 representing the minimum percent match a domain must map to the fusion transcript to be displayed. The corresponding environment variable is ``MAVIS_MIN_DOMAIN_MAPPING_MATCH`` and the default value is ``0.9``

    min_double_aligned_to_estimate_insertion_size
        :class:`int` - The minimum number of reads which map soft-clipped to both breakpoints to assume the size of the untemplated sequence between the breakpoints is at most the read length - 2 * min_softclipping. The corresponding environment variable is ``MAVIS_MIN_DOUBLE_ALIGNED_TO_ESTIMATE_INSERTION_SIZE`` and the default value is ``2``

    min_flanking_pairs_resolution
        :class:`int` - The minimum number of flanking reads required to call a breakpoint by flanking evidence. The corresponding environment variable is ``MAVIS_MIN_FLANKING_PAIRS_RESOLUTION`` and the default value is ``10``

    min_linking_split_reads
        :class:`int` - The minimum number of split reads which aligned to both breakpoints. The corresponding environment variable is ``MAVIS_MIN_LINKING_SPLIT_READS`` and the default value is ``2``

    min_mapping_quality
        :class:`int` - The minimum mapping quality of reads to be used as evidence. The corresponding environment variable is ``MAVIS_MIN_MAPPING_QUALITY`` and the default value is ``5``

    min_non_target_aligned_split_reads
        :class:`int` - The minimum number of split reads aligned to a breakpoint by the input bam and no forced by local alignment to the target region to call a breakpoint by split read evidence. The corresponding environment variable is ``MAVIS_MIN_NON_TARGET_ALIGNED_SPLIT_READS`` and the default value is ``1``

    min_orf_size
        :class:`int` - The minimum length (in base pairs) to retain a putative open reading frame (orf). The corresponding environment variable is ``MAVIS_MIN_ORF_SIZE`` and the default value is ``300``

    min_sample_size_to_apply_percentage
        :class:`int` - Minimum number of aligned bases to compute a match percent. if there are less than this number of aligned bases (match or mismatch) the percent comparator is not used. The corresponding environment variable is ``MAVIS_MIN_SAMPLE_SIZE_TO_APPLY_PERCENTAGE`` and the default value is ``10``

    min_softclipping
        :class:`int` - Minimum number of soft-clipped bases required for a read to be used as soft-clipped evidence. The corresponding environment variable is ``MAVIS_MIN_SOFTCLIPPING`` and the default value is ``6``

    min_spanning_reads_resolution
        :class:`int` - Minimum number of spanning reads required to call an event by spanning evidence. The corresponding environment variable is ``MAVIS_MIN_SPANNING_READS_RESOLUTION`` and the default value is ``5``

    min_splits_reads_resolution
        :class:`int` - Minimum number of split reads required to call a breakpoint by split reads. The corresponding environment variable is ``MAVIS_MIN_SPLITS_READS_RESOLUTION`` and the default value is ``3``

    novel_exon_color
        :class:`str` - Novel exon fill color. The corresponding environment variable is ``MAVIS_NOVEL_EXON_COLOR`` and the default value is ``'#000000'``

    outer_window_min_event_size
        :class:`int` - The minimum size of an event in order for flanking read evidence to be collected. The corresponding environment variable is ``MAVIS_OUTER_WINDOW_MIN_EVENT_SIZE`` and the default value is ``125``

    queue
        :class:`str` - The queue jobs are to be submitted to. The corresponding environment variable is ``MAVIS_QUEUE`` and the default value is ``''``

    scaffold_color
        :class:`str` - The color used for the gene/transcripts scaffolds. The corresponding environment variable is ``MAVIS_SCAFFOLD_COLOR`` and the default value is ``'#000000'``

    scheduler
        :class:`~mavis.submit.SCHEDULER` - The scheduler being used. The corresponding environment variable is ``MAVIS_SCHEDULER`` and the default value is ``'SLURM'``. Accepted values include: ``'SGE'``, ``'SLURM'``

    spanning_call_distance
        :class:`int` - The maximum distance allowed between breakpoint pairs (called by spanning reads) in order for them to pair. The corresponding environment variable is ``MAVIS_SPANNING_CALL_DISTANCE`` and the default value is ``5``

    splice_color
        :class:`str` - Splicing lines color. The corresponding environment variable is ``MAVIS_SPLICE_COLOR`` and the default value is ``'#000000'``

    split_call_distance
        :class:`int` - The maximum distance allowed between breakpoint pairs (called by split reads) in order for them to pair. The corresponding environment variable is ``MAVIS_SPLIT_CALL_DISTANCE`` and the default value is ``10``

    stdev_count_abnormal
        :class:`float` - The number of standard deviations away from the normal considered expected and therefore not qualifying as flanking reads. The corresponding environment variable is ``MAVIS_STDEV_COUNT_ABNORMAL`` and the default value is ``3.0``

    strand_determining_read
        :class:`int` - 1 or 2. the read in the pair which determines if (assuming a stranded protocol) the first or second read in the pair matches the strand sequenced. The corresponding environment variable is ``MAVIS_STRAND_DETERMINING_READ`` and the default value is ``2``

    time_limit
        :class:`int` - The time in seconds any given jobs is allowed. The corresponding environment variable is ``MAVIS_TIME_LIMIT`` and the default value is ``57600``

    trans_fetch_reads_limit
        :class:`nullable_int` - Related to :term:`fetch_reads_limit`. overrides fetch_reads_limit for transcriptome libraries when set. if this has a value of none then fetch_reads_limit will be used for transcriptome libraries instead. The corresponding environment variable is ``MAVIS_TRANS_FETCH_READS_LIMIT`` and the default value is ``12000``

    trans_min_mapping_quality
        :class:`nullable_int` - Related to :term:`min_mapping_quality`. overrides the min_mapping_quality if the library is a transcriptome and this is set to any number not none. if this value is none, min_mapping_quality is used for transcriptomes aswell as genomes. The corresponding environment variable is ``MAVIS_TRANS_MIN_MAPPING_QUALITY`` and the default value is ``1``

    trans_validation_memory
        :class:`int` - Default memory limit (mb) for the validation stage (for transcriptomes). The corresponding environment variable is ``MAVIS_TRANS_VALIDATION_MEMORY`` and the default value is ``18000``

    uninformative_filter
        :class:`bool` - Flag that determines if breakpoint pairs which are not within max_proximity to any annotations are filtered out prior to clustering. The corresponding environment variable is ``MAVIS_UNINFORMATIVE_FILTER`` and the default value is ``False``

    validation_memory
        :class:`int` - Default memory limit (mb) for the validation stage. The corresponding environment variable is ``MAVIS_VALIDATION_MEMORY`` and the default value is ``16000``

    width
        :class:`int` - The drawing width in pixels. The corresponding environment variable is ``MAVIS_WIDTH`` and the default value is ``1000``

    write_evidence_files
        :class:`bool` - Write the intermediate bam and bed files containing the raw evidence collected and contigs aligned. not required for subsequent steps but can be useful in debugging and deep investigation of events. The corresponding environment variable is ``MAVIS_WRITE_EVIDENCE_FILES`` and the default value is ``True``

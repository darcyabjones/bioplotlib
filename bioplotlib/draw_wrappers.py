from gene_shapes import Triangle
from gene_shapes import OpenTriangle

import matplotlib.patches as patches
from matplotlib.path import Path
from matplotlib.text import Text

def draw_region(
        seq,
        start=None,
        end=None,
        intron_threshold=1,
        exon=Triangle(width=1),
        intron=OpenTriangle(width=0.5, y_offset=0.5),
        other_shapes=dict(),
        names_to_print=dict(),
        ):
    """

    Keyword arguments:
    names_to_print -- dict.
    """
    if start is None:
        start = 0
    if end is None:
        end = len(seq)
    feature_patches = list()
    text_patches = list()
    for feature in seq[start:end].features:
        if feature.id in names_to_print:
            if 's' not in names_to_print[feature.id]:
                names_to_print[feature.id]['s'] = feature.id
            start = feature.location.start
            end = feature.location.end
            names_to_print[feature.id]['x'] = start + 0.5 * (end - start)
            text_patches.append(names_to_print[feature.id])
        if feature.type == 'CDS' and exon is not None:
            exons = list()
            introns = list()
            reverse = feature.strand == -1
            parts = sorted(
                feature.location.parts,
                key=lambda f: min(f.start, f.end),
                reverse=reverse
                )
            for i in range(len(parts)):
                strand = parts[i].strand
                # Draw intron if not the last exon
                if i > 0 and intron is not None:
                    if strand in {None, 0, 1}:
                        strand = 1
                        start = parts[i - 1].end
                        distance = (parts[i].start - parts[i - 1].end)
                    else:
                        strand = -1
                        start = parts[i - 1].start
                        distance = (parts[i].end - parts[i - 1].start)
                    if abs(distance) >= intron_threshold:
                        incl_intron = True
                        verts, codes = intron(
                            start,
                            0.,
                            distance
                            )
                        introns.append([start, distance])
                        p = Path(verts, codes)
                        feature_patches.append(
                            patches.PathPatch(
                                p,
                                **intron.properties
                                )
                            )
                    else:
                        incl_intron = False

                # Now draw the exon
                start = parts[i].start
                if strand in {None, 0, 1}:
                    strand = 1
                    start = parts[i].start
                else:
                    strand = -1
                    start = parts[i].end
                distance = (parts[i].end - parts[i].start) * strand

                if len(exons) == 0 or incl_intron:
                    exons.append([start, distance])
                else:  # Join two exons
                    exons[-1][1] += distance

                for e in exons:
                    verts, codes = exon(e[0], 0., e[1])
                    p = Path(verts, codes)
                    feature_patches.append(
                        patches.PathPatch(
                            p,
                            **exon.properties
                            )
                        )

        elif feature.type in other_shapes:
            part = feature.location
            strand = part.strand
            if strand in {None, 0, 1}:
                strand = 1
                start = part.start
            else:
                strand = -1
                start = part.end
            distance = (part.end - part.start) * strand

            verts, codes = other_shapes[feature.type](start, 0., distance)
            p = Path(verts, codes)
            feature_patches.append(
                patches.PathPatch(
                    p,
                    **other_shapes[feature.type].properties
                    )
                )

    return feature_patches, text_patches

def draw_region(
        seq,
        start=None,
        end=None,
        intron_threshold=1,
        exon=Triangle(width=1),
        intron=OpenTriangle(width=0.5, y_offset=0.5),
        other_shapes=dict(),
        names_to_print=dict(),
        ):
    """

    Keyword arguments:
    names_to_print -- dict.
    """
    if start is None:
        start = 0
    if end is None:
        end = len(seq)
    feature_patches = list()
    text_patches = list()
    for feature in seq[start:end].features:
        if feature.id in names_to_print:
            if 's' not in names_to_print[feature.id]:
                names_to_print[feature.id]['s'] = feature.id
            start = feature.location.start
            end = feature.location.end
            names_to_print[feature.id]['x'] = start + 0.5 * (end - start)
            text_patches.append(names_to_print[feature.id])
        if feature.type == 'CDS' and exon is not None:
            exons = list()
            introns = list()
            reverse = feature.strand == -1
            parts = sorted(
                feature.location.parts,
                key=lambda f: min(f.start, f.end),
                reverse=reverse
                )
            for i in range(len(parts)):
                strand = parts[i].strand
                # Draw intron if not the last exon
                if i > 0 and intron is not None:
                    if strand in {None, 0, 1}:
                        strand = 1
                        start = parts[i - 1].end
                        distance = (parts[i].start - parts[i - 1].end)
                    else:
                        strand = -1
                        start = parts[i - 1].start
                        distance = (parts[i].end - parts[i - 1].start)
                    if abs(distance) >= intron_threshold:
                        incl_intron = True
                        verts, codes = intron(
                            start,
                            0.,
                            distance
                            )
                        introns.append([start, distance])
                        p = Path(verts, codes)
                        feature_patches.append(
                            patches.PathPatch(
                                p,
                                **intron.properties
                                )
                            )
                    else:
                        incl_intron = False

                # Now draw the exon
                start = parts[i].start
                if strand in {None, 0, 1}:
                    strand = 1
                    start = parts[i].start
                else:
                    strand = -1
                    start = parts[i].end
                distance = (parts[i].end - parts[i].start) * strand

                if len(exons) == 0 or incl_intron:
                    exons.append([start, distance])
                else:  # Join two exons
                    exons[-1][1] += distance

                for e in exons:
                    verts, codes = exon(e[0], 0., e[1])
                    p = Path(verts, codes)
                    feature_patches.append(
                        patches.PathPatch(
                            p,
                            **exon.properties
                            )
                        )

        elif feature.type in other_shapes:
            part = feature.location
            strand = part.strand
            if strand in {None, 0, 1}:
                strand = 1
                start = part.start
            else:
                strand = -1
                start = part.end
            distance = (part.end - part.start) * strand

            verts, codes = other_shapes[feature.type](start, 0., distance)
            p = Path(verts, codes)
            feature_patches.append(
                patches.PathPatch(
                    p,
                    **other_shapes[feature.type].properties
                    )
                )

    return feature_patches, text_patches

def draw_synteny(
        fig,
        isolates,
        data,
        shapes=dict(),
        xlims=dict(),
        ylims=dict(),
        names_to_print=dict(),
        between=True,
        within=False,
        between_color='',
        within_color='',
        hspace=2,
        ):
    """
    Keyword arguments:
    fig -- the matplotlib figure instance to plot to
    isolates -- a list of which isolates to plot, in the order to be plotted
    data -- a dictionary keyed by isolate with dict of lists of BioPython SeqRecords or tracks to plot
        isolate: {
            'Genes': [SeqRecord, SeqRecord, ...], # gene track
            'gc': [np.array, np.array, ...], # plot track
            }
        Must have _at least_ the 'Genes' track.
    shapes -- a dictionary keyed by feature type with shape objects to use for that feature.
    xlims -- scaffold xlims, dict keyed by scaffold id with (start, end, interval) tuples
    ylims -- dict of ylims keyed by axes id's
    names_to_print -- dict of names to print and kwargs to send to the text instance
    between -- Boolean, plot alignments between
    between_color -- hex colour to use for between alignments, if a list is given will use alternatingly (by isolate)
    within -- Boolean, plot alignments on same scaffold
    within_color -- hex colour to use for within alignments, if a list is given will use alternatingly (by scaffold)
    """

    # Figure out the scaffold ratios
    max_length = 0
    pdata = list()
    for isolate in isolates:
        this_data = dict()
        scaffolds = data[isolate]['Genes']
        scaffold_lengths = [len(s) for s in scaffolds]
        for i, scaf in enumerate(scaffolds):
            if scaf.id in xlims:
                scaffold_lengths[i] = abs(xlims[scaf][0] - xlims[scaf][1])

        this_data['data'] = data[isolate]
        this_data['length'] = sum(scaffold_lengths)
        if this_data['length'] > max_length:
            max_length = this_data['length']
        this_data['y_ratio'] = len(data[isolate]) # How many tracks per isolate
        pdata.append(this_data)
    for d in pdata:
        d['lengths'].append(max_length - d['length'])
        d['ratios'] = [s / max_length for s in d['lengths']]


    ### Edit y ratios here
    ### Edit yticks here
    ### Edit yticklabels here

    ratios = [d['y_ratio'] for d in pdata]
    gs = gridspec.GridSpec(len(isolates), 1, hspace=hspace, height_ratios=ratios)

    for i, isolate in enumerate(isolates):
        sgs = gridspec.GridSpecFromSubplotSpec(
            len(pdata[i]['data']), len(pdata[i]['lengths']),
            subplot_spec=gs[i],
            width_ratios=pdata[i]['ratios'],
            )
        pdata[i]['gs'] = sgs

    region_params = {
        'mnh120_REPET_TEs': Triangle(width=0.9, y_offset=0.05, facecolor=cat_colours[1], linewidth=0),
        'mnh120_REPET_SSRs': Triangle(width=0.9, y_offset=0.05, facecolor=cat_colours[3], linewidth=0),
        }

    axes = defaultdict(lambda: defaultdict(dict))
    title_font = {'fontsize': 10, 'verticalalignment': 'baseline'}

    for isolate, d in zip(isolates, pdata):
        scaffolds = d['scaffolds']
        sgs = d['gs']
        data = d['data']
        for i, scaffold in enumerate(data['Genes']):
            ax = fig.add_subplot(sgs[i, 1])
            axes[isolate][scaffold.id] = ax
            d['ax'].patch.set_fill(False)

            d['ax'].set_title(scaf_name, loc='left', fontdict=title_font)

            seq = GENOMES[isolate][scaffold]
            if scaffold in xlims:
                d['ax'].set_xlim(*xlims[scaffold])
            else:
                d['ax'].set_xlim(0, len(seq))
            d['ax'].set_xticks(tick_formatter(d['ax'], interval=x_interval))
            if isolate in region_params:
                shapes = region_params[isolate]
            else:
                shapes = {
                    'exon': Triangle(
                        width=0.9,
                        y_offset=0.05,
                        fill=True,
                        facecolor='black',
                        edgecolor='none'
                        ),
                    'intron': OpenTriangle(
                        width=0.45,
                        y_offset=0.5,
                        fill=False
                        ),
                    'other_shapes': {
                        'mnh120_REPET_TEs': Triangle(
                            width=0.9,
                            y_offset=0.05,
                            facecolor=cat_colours[1],
                            linewidth=0
                            ),
                        }
                    }
            d['ax'].set_ylim(0, d['y_ratio'])
            d['ax'].set_yticks(d['yticks'])
            d['ax'].set_yticklabels(d['yticklabels'])

            feature_patches, feature_texts = draw_region(
                seq,
                names_to_print=names_to_print,
                **shapes
                )
            for patch in feature_patches:
                d['ax'].add_patch(patch)
            for text in feature_texts:
                d['ax'].text(**text)

    ### Set which links to plot and in what order, refers to index of `isolates` list
    comparisons = [(0, 1), (1, 2), (2, 3)]
    min_psim = 0
    min_pid = 85

    for i, j in comparisons:
        risolate = isolates[i]
        qisolate = isolates[j]
        for rscaffold in pdata[i]['scaffolds']:
            for qscaffold in pdata[j]['scaffolds']:
                if i == 0 or i == j:
                    y1_range = [1, 0]
                elif i == len(isolates) - 1:
                    y1_range = [0, 1]
                else:
                    if i < j:
                        y1_range = [0.5, 0]
                    else:
                        y1_range = [1, 0.5]
                if j == 0 or i == j:
                    y2_range = [1, 0]
                elif j == len(isolates) - 1:
                    y2_range = [0, 1]
                else:
                    if j < i:
                        y2_range = [0.5, 0]
                    else:
                        y2_range = [0.5, 1]
                if i % 2 == 0:
                    facecolor = cat_colours[3]
                else:
                    facecolor = cat_colours[0]
                slink = CrossLink(
                    ax1=pdata[i]['ax'],
                    ax2=pdata[j]['ax'],
                    y1_range=y1_range,
                    y2_range=y2_range,
                    alpha=0.2,
                    linewidth=0.,
                    zorder=0,
                    facecolor=facecolor,
                    )
                with open(
                        promer_files[rscaffold][qscaffold]['coords'],
                        'r') as handle:
                    for link in read_promer_coords(handle):
                        if link_limits(link[qscaffold], pdata[j]['ax']) and \
                                link_limits(link[rscaffold], pdata[i]['ax']) and \
                                link['psim'] >= min_psim and \
                                link['pid'] >= min_pid:
                            patch = slink(
                                x1_start=link[rscaffold]['start'],
                                x1_length=link[rscaffold]['length'],
                                x2_start=link[qscaffold]['start'],
                                x2_length=link[qscaffold]['length'],
                                alpha=link["psim"]/1000
                                )
fig.savefig('combined-zoom.svg')
fig.savefig('combined-zoom.png', dpi=600)
fig.show()

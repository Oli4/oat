import imageio
import functools
import numpy as np
from struct import unpack

def get_cfp(filepath):
    """

    :param filepath:
    :return:
    """
    return imageio.imread(filepath)


class OCT():
    def __init__(self, bscans, nir, meta):
        self._bscans = bscans
        self._nir = nir
        self._meta = meta

    def __getitem__(self, key):
        return self._bscans[key]

    @property
    def segmentation(self):
        segmentations = np.stack([bscan._segmentation for bscan in self._bscans])
        # It seems like there is no standard structure in the exported segmentations from HEYEX
        #seg_mapping = {"ILM":0,"GCL":2, "BM":1, "IPl":3, "INL":4, "IPL":5, "ONL":6, "ELM":8, "EZ/PR1":14, "IZ/PR2":15,
        #               "RPE":16}
        # return {k: segmentations[:, seg_mapping[k], :] for k in seg_mapping}
        return {"{}".format(i): segmentations[:, i, :] for i in range(segmentations.shape[1])}

    @property
    def meta(self):
        return self._meta

    @property
    def bscan_meta(self):
        return [bs._meta for bs in self._bscans]
    @property
    def volume(self):
        return np.stack([x._scan for x in self._bscans], axis=-1)

    @property
    def nir(self):
        return self._nir

    @classmethod
    def read_vol(cls, filepath):
        meta = cls.get_vol_header(filepath)
        nir = cls.get_slo_image(filepath)
        bscans = cls.get_bscan_images(filepath)

        return cls(bscans, nir, meta)

    @classmethod
    def read_xml(cls, filepath):
        #return cls(bscans, nir, meta)
        pass

    @staticmethod
    @functools.lru_cache(maxsize=4, typed=False)
    def get_bscan_images(filepath):
        """

        :param filepath:
        :return:

        The specification of the B-scan header shown below was found in:
        https://github.com/FabianRathke/octSegmentation/blob/master/collector/HDEVolImporter.m

        {'Version','c',0}, ... 		    % Version identifier (zero terminated string). Version Format: "HSF-BS-xxx,
                                          xxx = version number of the B-Scan header format. Current version: xxx = 103
        {'BScanHdrSize','i',12}, ...	% Size of the B-Scan header in bytes. It is identical to the same value of the
                                          file header.
        {'StartX','d',16}, ...		    % X-Coordinate of the B-Scan's start point in mm.
        {'StartY','d',24}, ...		    % Y-Coordinate of the B-Scan's start point in mm.
        {'EndX','d',32}, ...			% X-Coordinate of the B-Scan's end point in mm. For circle scans, this is the
                                          X-Coordinate of the circle's center point.
        {'EndY','d',40}, ...			% Y-Coordinate of the B-Scan's end point in mm. For circle scans, this is the
                                          Y-Coordinate of the circle's center point.
        {'NumSeg','i',48}, ...		    % Number of segmentation vectors
        {'OffSeg','i',52}, ...		    % Offset of the array of segmentation vectors relative to the beginning of this
                                          B-Scan header.
        {'Quality','f',56}, ...		    % Image quality measure. If this value does not exist, its value is set to INVALID.
        {'Shift','i',60}, ...			% Horizontal shift (in # of A-Scans) of the classification band against the
                                          segmentation lines (for circular scan only).
        {'IVTrafo','f',64}, ...		    % Intra volume transformation matrix. The values are only available for volume and
                                          radial scans and if alignment is turned off, otherwise the values are initialized
                                          to 0.
        {'Spare','c',88}};              % Spare bytes for future use.
        """
        hdr = OCT.get_vol_header(filepath)

        with open(filepath, mode='rb') as myfile:
            fileContent = myfile.read()

        # Calculate offset
        slo_size = hdr['SizeXSlo'] * hdr['SizeYSlo']
        header_size = 2048

        bscan_size = hdr['SizeX'] * hdr['SizeZ']

        bscans = []

        for b in range(hdr['NumBScans']):
            header_offset = header_size + slo_size + b * (4 * bscan_size) + ((b) * hdr['BScanHdrSize'])
            bscan_offset = header_offset + hdr['BScanHdrSize']

            # Read B-scan header
            header_tail_size = hdr['BScanHdrSize'] - 68
            bs_header = unpack("=12siddddiifif" + str(header_tail_size) + "s",
                               fileContent[header_offset:header_offset + hdr['BScanHdrSize']])
            hdr_b = {'Version': bs_header[0].rstrip(),
                     'BScanHdrSize': bs_header[1],
                     'StartX': bs_header[2],
                     'StartY': bs_header[3],
                     'EndX': bs_header[4],
                     'EndY': bs_header[5],
                     'NumSeg': bs_header[6],
                     'OffSeg': bs_header[7],
                     'Quality': bs_header[8],
                     'Shift': bs_header[9],
                     'IVTrafo': bs_header[10]}

            # Read seg lines
            seg_size = hdr_b['NumSeg'] * hdr['SizeX']
            seg_offset = header_offset + hdr_b['OffSeg']
            seg_lines = unpack(
                '=' + str(seg_size) + 'f', fileContent[seg_offset:(seg_offset + (seg_size * 4))])
            seg_lines = np.asarray(seg_lines, dtype='float32')
            seg_lines = seg_lines.reshape(hdr_b['NumSeg'], hdr['SizeX'])

            bscan_img = unpack(
                '=' + str(bscan_size) + 'f', fileContent[bscan_offset:(bscan_offset + (bscan_size * 4))])
            bscan_img = np.asarray(bscan_img, dtype='float32')
            bscan_img[bscan_img > 1] = 0
            bscan_img = bscan_img.reshape(hdr['SizeZ'], hdr['SizeX'])

            bscan = Bscan((bscan_img * 255).astype("uint8"), seg_lines, hdr_b)
            bscans.append(bscan)

        return bscans

    @staticmethod
    @functools.lru_cache(maxsize=4, typed=False)
    def get_vol_header(filepath):
        """ Read the header of the .vol file and return it as a Python dictionary.

        :param filepath:
        :return:

        The specification for the file header shown below was found in
        https://github.com/FabianRathke/octSegmentation/blob/master/collector/HDEVolImporter.m

        {'Version','c',0}, ... 		    % Version identifier: HSF-OCT-xxx, xxx = version number of the file format,
                                          Current version: xxx = 103
        {'SizeX','i',12},  ... 			% Number of A-Scans in each B-Scan, i.e. the width of each B-Scan in pixel
        {'NumBScans','i',16}, ... 		% Number of B-Scans in OCT scan
        {'SizeZ','i',20}, ... 			% Number of samples in an A-Scan, i.e. the Height of each B-Scan in pixel
        {'ScaleX','d',24}, ... 			% Width of a B-Scan pixel in mm
        {'Distance','d',32}, ... 		% Distance between two adjacent B-Scans in mm
        {'ScaleZ','d',40}, ... 			% Height of a B-Scan pixel in mm
        {'SizeXSlo','i',48}, ...  		% Width of the SLO image in pixel
        {'SizeYSlo','i',52}, ... 		% Height of the SLO image in pixel
        {'ScaleXSlo','d',56}, ... 		% Width of a pixel in the SLO image in mm
        {'ScaleYSlo','d',64}, ...		% Height of a pixel in the SLO image in mm
        {'FieldSizeSlo','i',72}, ... 	% Horizontal field size of the SLO image in dgr
        {'ScanFocus','d',76}, ...		% Scan focus in dpt
        {'ScanPosition','c',84}, ... 	% Examined eye (zero terminated string). "OS" for left eye; "OD" for right eye
        {'ExamTime','i',88}, ... 		% Examination time. The structure holds an unsigned 64-bit date and time value and
                                          represents the number of 100-nanosecond units	since the beginning of January 1, 1601.
        {'ScanPattern','i',96}, ...		% Scan pattern type: 0 = Unknown pattern, 1 = Single line scan (one B-Scan only),
                                          2 = Circular scan (one B-Scan only), 3 = Volume scan in ART mode,
                                          4 = Fast volume scan, 5 = Radial scan (aka. star pattern)
        {'BScanHdrSize','i',100}, ...	% Size of the Header preceding each B-Scan in bytes
        {'ID','c',104}, ...				% Unique identifier of this OCT-scan (zero terminated string). This is identical to
                                          the number <SerID> that is part of the file name. Format: n[.m] n and m are
                                          numbers. The extension .m exists only for ScanPattern 1 and 2. Examples: 2390, 3433.2
        {'ReferenceID','c',120}, ...	% Unique identifier of the reference OCT-scan (zero terminated string). Format:
                                          see ID, This ID is only present if the OCT-scan is part of a progression otherwise
                                          this string is empty. For the reference scan of a progression ID and ReferenceID
                                          are identical.
        {'PID','i',136}, ...			% Internal patient ID used by HEYEX.
        {'PatientID','c',140}, ...		% User-defined patient ID (zero terminated string).
        {'Padding','c',161}, ...		% To align next member to 4-byte boundary.
        {'DOB','date',164}, ... 		% Patient's date of birth
        {'VID','i',172}, ...			% Internal visit ID used by HEYEX.
        {'VisitID','c',176}, ...		% User-defined visit ID (zero terminated string). This ID can be defined in the
                                          Comment-field of the Diagnosis-tab of the Examination Data dialog box. The VisitID
                                          must be defined in the first row of the comment field. It has to begin with an "#"
                                          and ends with any white-space character. It can contain up to 23 alpha-numeric
                                          characters (excluding the "#").
        {'VisitDate','date',200}, ...	% Date the visit took place. Identical to the date of an examination tab in HEYEX.
        {'GridType','i',208}, ...		% Type of grid used to derive thickness data. 0 No thickness data available,
                                          >0 Type of grid used to derive thickness  values. Seeter "Thickness Grid"	for more
                                          details on thickness data, Thickness data is only available for ScanPattern 3 and 4.
        {'GridOffset','i',212}, ...		% File offset of the thickness data in the file. If GridType is 0, GridOffset is 0.
        {'GridType1','i',216}, ...		% Type of a 2nd grid used to derive a 2nd set of thickness data.
        {'GridOffset1','i',220}, ...	% File offset of the 2 nd thickness data set in the file.
        {'ProgID','c',224}, ...			% Internal progression ID (zero terminated string). All scans of the same
                                          progression share this ID.
        {'Spare','c',258}}; 			% Spare bytes for future use. Initialized to 0.


        """

        # Read binary file
        with open(filepath, mode='rb') as myfile:
            fileContent = myfile.read()

        # Read raw hdr
        Version, SizeX, NumBScans, SizeZ, ScaleX, Distance, ScaleZ, SizeXSlo, \
        SizeYSlo, ScaleXSlo, ScaleYSlo, FieldSizeSlo, ScanFocus, ScanPosition, \
        ExamTime, ScanPattern, BScanHdrSize, ID, ReferenceID, PID, PatientID, \
        Padding, DOB, VID, VisitID, VisitDate, GridType, GridOffset, GridType1, \
        GridOffset1, ProgID, Spare = unpack(
            "=12siiidddiiddid4sQii16s16si21s3sdi24sdiiii34s1790s", fileContent[:2048])

        # Format hdr properly
        hdr = {'Version': Version.decode('ascii').replace('\x00', ''),
               'SizeX': SizeX,
               'NumBScans': NumBScans,
               'SizeZ': SizeZ,
               'ScaleX': ScaleX,
               'Distance': Distance,
               'ScaleZ': ScaleZ,
               'SizeXSlo': SizeXSlo,
               'SizeYSlo': SizeYSlo,
               'ScaleXSlo': ScaleXSlo,
               'ScaleYSlo': ScaleYSlo,
               'FieldSizeSlo': FieldSizeSlo,
               'ScanFocus': ScanFocus,
               'ScanPosition': ScanPosition.decode('ascii').replace('\x00', ''),
               'ExamTime': ExamTime,
               'ScanPattern': ScanPattern,
               'BScanHdrSize': BScanHdrSize,
               'ID': ID.decode('ascii').replace('\x00', ''),
               'ReferenceID': ReferenceID.decode('ascii').replace('\x00', ''),
               'PID': PID,
               'PatientID': PatientID.decode('ascii').replace('\x00', ''),
               'DOB': DOB,
               'VID': VID,
               'VisitID': VisitID.decode('ascii').replace('\x00', ''),
               'VisitDate': VisitDate,
               'GridType': GridType,
               'GridOffset': GridOffset,
               'GridType1': GridType1,
               'GridOffset1': GridOffset1,
               'ProgID': ProgID.decode('ascii').replace('\x00', '')}

        return hdr

    @classmethod
    @functools.lru_cache(maxsize=4, typed=False)
    def get_slo_image(cls, filepath):
        """

        :param filepath:
        :return:
        """
        hdr = OCT.get_vol_header(filepath)

        with open(filepath, mode='rb') as myfile:
            fileContent = myfile.read()

        # Read SLO image
        size_x_slo = hdr['SizeXSlo']
        size_y_slo = hdr['SizeYSlo']
        slo_size = size_x_slo * size_y_slo
        slo_offset = 2048
        slo_img = unpack(
            '=' + str(slo_size) + 'B', fileContent[slo_offset:(slo_offset + slo_size)])
        slo_img = np.asarray(slo_img, dtype='uint8')
        slo_img = slo_img.reshape(size_x_slo, size_y_slo)
        return slo_img


class Bscan():
    def __init__(self, scan, segmentation, meta):
        self._scan = scan
        self._segmentation = segmentation
        self._meta = meta


{% macro add_table(table) -%}
{% for i in range(table.nrows) -%}
{% if i == 0 -%}
{% for cell in table.row_values(i) -%}
        |{{ cell }}
{%- endfor %}|
{% for j in range(table.ncols) -%}
            |-
{%- endfor %}|
{%- else %}
{% for cell in table.row_values(i) -%}
     |{{ cell }}
{%- endfor %}|
{%- endif %}
{%- endfor %}
{%- endmacro -%}

{%- macro getName(path) -%}
{% set item = path.split("/")[-3].rsplit("_",1)[0] -%}
{{ item }}
{%- endmacro -%}

{% macro baseimg(img) %}
{% set fb = open(img,'r') %}
{% set bfb = base64(fb.read()) %}
{{ bfb }}
{% endmacro %}

{%- macro addImg(images) %}
<div class="clear boxCIB01">
          <div class="ban" id="demo1">
            <div class="ban2" id="ban_pic1">
              <div class="prev1" id="prev1"><img src="./images/index_tab_l.png" alt="" width="28" height="51"></div>
              <div class="next1" id="next1"><img src="./images/index_tab_r.png" alt="" width="28" height="51"></div>
              <ul style="width: 1600px; left: 0px;">
{% for item in images %}
                        <li class="slide" style="float: left;"><a title="{{ getName(item) }}" href="javascript:;" class="img-toggle"><img src="data:image/png;base64,{{ baseimg(item) }}" alt="" width="600" height="500"></a></li>

{% endfor %}
              </ul>
            </div>
            <div class="min_pic">
              <div class="prev_btn1" id="prev_btn1"><img src="./images/feel3.png" alt="" width="9" height="18"></div>
              <div class="next_btn1" id="next_btn1"><img src="./images/feel4.png" alt="" width="9" height="18"></div>
              <div class="num clearfix smallbox" id="ban_num1">
              <ul style="width: 184px; height: 164px; left: 35%;">

{% for i in range(images|length) %}
{% if i == 0 %}
                        <li class="slide on" style="float: left;"><a title="{{ getName(images[0]) }}}" href="javascript:;" class="img-toggle"><img src="data:image/png;base64,{{ baseimg(images[0])}}" alt="" width="600" height="500"></a></li>
{% else %}
                        <li class="slide" style="float: left;"><a title="{{ getName(images[i]) }}" href="javascript:;" class="img-toggle"><img src="data:image/png;base64,{{ baseimg(images[i]) }}" alt="" width="600" height="500"></a></li>


{% endif %}
{% endfor %}
              </ul>
              </div>
            </div>
          </div>
          <div class="mhc"></div>
        </div>
{% endmacro -%}

## 中科院计算所 • 北京中科晶云科技有限公司

## 原始数据质量评估报告

## 1.质控介绍
数据质控，旨在查看原始数据质量信息，包括原始数据q20,q30,gc含量等。


## 2.数据分析流程

利用`fastqc`对每个fastq文件进行质量统计，并汇总每个fastq的信息


##3 具体分析及结果统计

###3.1 测序质量评估

####3.1.1 原始序列数据

高通量测序(如Illumina HiSeqTM4000/MiseqTM/X-Ten)得到的原始图像数据文件经碱基识别(Base Calling)分析转化为原始测序序列(Sequenced Reads)，我们称之为 Raw Data或Raw Reads，结果以 FASTQ (简称为fq)文件格式存储，其中包含测序序列(reads)的序列信息以及其对应的测序质量信息。

FASTQ格式文件中每个read由四行描述，如下：

|   |
| ----------------------------------------------------------------------------------------------------------------------- |
| @ST-E00600:21:H2HYGALXX:1:1101:1307:1000 1:N:0:ACCTCCAA  |
|  GGAAATGCCCTGTCCACACAGGATAGAAAAGTGTGACCTCCGGGTTCAAGAATTTTGTAGTCCGTGATCCTGGGTGCACTGGCCCCATAGTTATTCTTACCCATGCTTCCTTCCTGTCATCGTTGACAAGCCCCAAGATATATTTCTAGT |
| +  |
|  AAJFFFFJJJJJJAJFJJAJJJJFFAJFJJ<JJJFJFFJAAJJJJJAJJAJJJAFJJFJJJFAJJAJAFJAFJJJJAJJJAJFJAFJ>JFJJJJAJJJJFJJJJJJAFJJJJJJJJJFJAAJJFJJFJ>FFAFFFJJJ-J-JJFJJJJJ- |


其中：

第一行以“@”开头，随后为Illumina 测序标识别符和描述文字；

第二行是碱基序列；

第三行以“+”开头，随后为Illumina 测序标识别符(选择性部分)；

第四行是对应碱基的测序质量，该行中每个字符对应的 ASCII 值减去 33，即为碱基质量值。

Illumina测序标识符详细信息如表3.2所示：


|   |   |
| ------------ | ------------------------------------------------------------------------------------------- |
| @ST-E00600  | Instrument - unique identifier of the sequencer  |
| 21  |  run number - Run number on instrument |
| H2HYGALXX  |  FlowCell ID - ID of flowcell |
| 1  |  LaneNumber - positive integer |
|  1101 | TileNumber - positive integer  |
| 1307  |  X - x coordinate of the spot. Integer which can be negative |
| 1000  |  Y - y coordinate of the spot. Integer which can be negative |
|  1 |  ReadNumber - 1 for single reads; 1 or 2 for paired ends |
| N  |  whether it is filtered - NB: Y if the read is filtered out, not in the delivered fastq file, N otherwise |
| 0  | control number - 0 when none of the control bits are on, otherwise it is an even number  |
|  ACCTCCAA |  Illumina index sequences |


####3.1.2 不同位置的碱基质量

在测序过程中会存在一定的错误率，测序错误率分布检查可以反映测序数据的质量。如果测序错误率用e表示，Illumina HiSeqTM4000/MiseqTM的碱基质量值用Qphred表示，则有：Qphred=-10log10(e)。

Illumina 1.9版本中碱基识别与Phred分值之间的简明对应关系见下表3.3所示：

<center>表3.3 Illumina测序标识符详细信息</center>

| Phred分值  |  不正确的碱基识别 |  碱基正确识别率 |  Q-sorce |
| ------------ | ------------ | ------------ | ------------ |
| 10  | 1/10     | 90%     | Q10  |
| 20  | 1/100    | 99%     | Q20  |
| 30  | 1/1000   | 99.9%   | Q30  |
| 40  | 1/10000  | 99.99%  | Q40  |

测序错误率分布具有以下两个特点：

a) 测序错误率会随着测序序列(Reads)长度的增加而升高，这是由测序过程中化学试剂的消耗导致的，并且此现象为illumina高通量测序平台的共有特征

b) 前10个碱基的位置也会发生较高的测序错误率，而这个长度也正好等于在建库过程中所需要的随机引物的长度。所以推测这部分碱基的测序错误率较高的原因是：随机引物与模版的不完全结合。一般情况下，单个碱基位置的测序错误率应该低于1%。

对本项目所有测序数据进行不同位置的碱基错误率进行评估，结果如图3.1所示，横轴为测序reads长度，虚线左边为R1端fastq错误率统计，虚线右边为R2端fastq错误率统计（如果为SE测序，则只有R1端错误率统计），纵轴为该位点的平均错误率。


使用FastQC工具对本课题中测序数据进行不同位置的碱基质量评估，结果如图3.2所示，横轴为测序reads长度，纵轴为质量得分

{{ addImg(per_base_quality) }}

<center>图3.2 测序样本的碱基质量分布</center>



####3.1.3碱基质量分布百分比

使用FastQC工具对本课题中测序数据进行碱基平均质量评估，结果如图3.3所示，横轴为测序质量，纵轴reads个数。

{{ addImg(per_sequence_quality) }}
<center>图3.3 测序样本的reads质量统计</center>


####3.1.4 Reads GC含量分布

使用FastQC工具对本课题中测序数据进行reads GC含量分布评估，结果如图3.4所示，横轴为测序质量，纵轴reads个数。

{{ addImg(per_sequence_gc_content) }}
<center>图3.4 测序样本的GC含量分布</center>


####3.1.5 Reads 碱基成分

鉴于序列的随机性打断和G/C、A/T含量分别相等的原则，理论上每个测序循环上的GC及AT含量应分别相等(若为链特异性建库，可能会出现AT分离和/或GC分离)，且在整个测序过程基本稳定不变，呈水平线。但在现有的高通量测序技术中，PCR所用的6bp的随机引物会引起前几个位置的核苷酸组成存在一定的偏好性，这种波动属于正常情况。

使用FastQC工具对本课题中测序数据进行reads GC含量密度分布评估，结果如图3.5所示，横轴为reads长度，纵轴为碱基频率

{{ addImg(per_base_sequence_content) }}

<center>图3.5 测序样本的碱基含量分布</center>


####3.1.6 Duplication百分比

使用FastQC工具对本课题中测序数据进行Reads重复率百分比评估，结果如图3.6所示，横轴为reads个数，纵轴为reads数占百分比。

{{ addImg(duplication_levels) }}
<center>图3.6 测序样本的reads重复百分比统计</center>

####3.1.7 数据质量汇总

原始测序数据经过数据过滤、错误率检查、碱基质量分布、reads质量分布、GC含量分布、PCR重复率统计、碱基含量分布等评估步骤，获得可以用于后续分析使用的clean reads。对质量评估后的数据质量进行汇总，如下表3.4所示。

<center>表3.4测序文件信息</center>

{{ add_table(table3_4) }}

1.Fastq_name : 测序样本fastq文件名，1为左端reads，2为右端reads。

2.Total_reads : 该Fastq测序数据过滤后的reads数 (即用于后续分析的数据，统计方法同Raw reads)。

3.Base_count：过滤后数据中的碱基数 (Clean reads数乘以序列长度,并转化为以G为单位)。

4.Error_rate：序列整体碱基错误率。

5.Q20：Phred数值大于20的碱基占总体碱基的比率。

6.Q30：Phred数值大于30的碱基占总体碱基的比率。

7.GC_content : 计算碱基G和C的数量总和占总体碱基数量的比率。

###3.4 附录文件

**(1).report文件夹：** reads的质控信息统计图，可查看各类质控统计数据，比对率等。

<div class="pop_up" id="demo2">
      <div class="pop_up_xx"><img src="./images/close.png" alt="关闭" width="40" height="40"></div>
      <div class="pop_up2" id="ban_pic2">
        <ul style="width: 500px;">
          <li><a href="javascript:;"><img width="500" height="500"></a>
            <p></p>
          </li>
        </ul>
      </div>
    </div>


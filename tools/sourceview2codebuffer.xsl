<?xml version="1.0"?>

<!--
    GtkSourceView to PyGTKCodeBuffer syntax-file converter.
    =======================================================

    Copyright 2008 
    Hannes Matuschek <hmatuschek@gmail.com>
    
    This file is distributed under the GNU LGPL license!
    Read LICENCE for more details.
    .......................................................

    This XSLT file converts GtkSourceView syntax-definitions into 
    PyGTKCodeBuffer syntax-files! Simply call:
        xsltproc sourceview2codebuffer.xsl [INPUTFILE.lang] 
    to convert a syntax-file!
-->


<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<!-- ROOT-TEPLATE -->
<xsl:template match="/">
    <xsl:comment>
        This syntax-file was generated by sourceview2codebuffer.xsl from
        GtkSourceView's <xsl:value-of select="/language/@_name"/>-syntax-file!
        
        This transformation is not perfect so it may need some hand-word to fix
        minor issues in this file.
        
        You can get sourceview2codebuffer.xsl from http://pygtkcodebuffer.googlecode.com/. 
    </xsl:comment>

    <syntax>
        <xsl:apply-templates />
    </syntax>
</xsl:template>


<!-- We specify escape-chars in <string>-tags -> ignore -->
<xsl:template match="escape-char" />


<!-- Handle <pattern-item>-tags -->
<xsl:template match="pattern-item">
    <pattern><xsl:call-template name="style-attr"/><xsl:value-of select="./regex"/></pattern>
</xsl:template>


<!-- Handle <keyword-list>s -->
<xsl:template match="keyword-list">
    <keywordlist>
        <xsl:call-template name="style-attr"/>
        <xsl:call-template name="flags-attr"/>
        <xsl:apply-templates />
    </keywordlist>
</xsl:template>

<xsl:template match="keyword-list/keyword">
    <keyword><xsl:value-of select="."/></keyword>
</xsl:template>


<!-- Handle <line-comment>s -->
<xsl:template match="line-comment">
    <pattern><xsl:call-template name="style-attr"/><xsl:value-of select="./start-regex"/>.*$</pattern>
</xsl:template>


<!-- handle <block-comment>s -->
<xsl:template match="block-comment">
    <string>
        <xsl:call-template name="style-attr"/>
        <starts><xsl:value-of select="./start-regex"/></starts>
        <ends><xsl:value-of select="./end-regex"/></ends>
    </string>
</xsl:template>


<!-- handle <string>s -->
<xsl:template match="string">
    <string>
        <xsl:call-template name="style-attr"/>
        <xsl:if test="/language/escape-char">
            <xsl:attribute name="escape"><xsl:value-of select="/language/escape-char"/></xsl:attribute>
        </xsl:if>
        <starts><xsl:value-of select="./start-regex"/></starts>
        <ends><xsl:value-of select="./end-regex"/></ends>
    </string>
</xsl:template>


<!-- handle <syntax-item>s -->
<xsl:template match="syntax-item">
    <string>
        <xsl:call-template name="style-attr"/>
        <starts><xsl:value-of select="./start-regex"/></starts>
        <ends><xsl:value-of select="./end-regex"/></ends>
    </string>
</xsl:template>


<xsl:template name="style-attr">
    <xsl:choose>
        <xsl:when test="./@style='Comment'">
            <xsl:attribute name="style">comment</xsl:attribute>
        </xsl:when>
        <xsl:when test="./@style='String'">
            <xsl:attribute name="style">string</xsl:attribute>
        </xsl:when>
        <xsl:when test="./@style='Preprocessor'">
            <xsl:attribute name="style">preprocessor</xsl:attribute>
        </xsl:when>
        <xsl:when test="./@style='Keyword'">
            <xsl:attribute name="style">keyword</xsl:attribute>
        </xsl:when>
        <xsl:when test="./@style='Data Type'">
            <xsl:attribute name="style">datatype</xsl:attribute>
        </xsl:when>
        <xsl:when test="./@style='Decimal'">
            <xsl:attribute name="style">number</xsl:attribute>
        </xsl:when>
        <xsl:when test="./@style='Floating Point'">
            <xsl:attribute name="style">number</xsl:attribute>
        </xsl:when>
        <xsl:when test="./@style='Base-N Integer'">
            <xsl:attribute name="style">number</xsl:attribute>
        </xsl:when>
        <xsl:when test="./@style='Character'">
            <xsl:attribute name="style">string</xsl:attribute>
        </xsl:when>
        <xsl:when test="./@style='Specials'">
            <xsl:attribute name="style">special</xsl:attribute>
        </xsl:when>
        <xsl:when test="./@style='Function'">
            <xsl:attribute name="style">function</xsl:attribute>
        </xsl:when>
        <xsl:when test="./@style='Others'">
            <xsl:attribute name="style">special</xsl:attribute>
        </xsl:when>
        <xsl:when test="./@style='Others 2'">
            <xsl:attribute name="style">special</xsl:attribute>
        </xsl:when>
        <xsl:when test="./@style='Others 3'">
            <xsl:attribute name="style">special</xsl:attribute>
        </xsl:when>
        
        <xsl:otherwise>
            <xsl:message>Unknwon style-name "<xsl:value-of select="./@style"/>"</xsl:message>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>


<xsl:template name="flags-attr">
    <xsl:attribute name="flags">
        <xsl:if test="./@case-sensitive='FALSE' or ./@case-sensitive='false'">I</xsl:if>
    </xsl:attribute>
</xsl:template>


</xsl:stylesheet>

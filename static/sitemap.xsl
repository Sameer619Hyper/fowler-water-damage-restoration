<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:sitemap="http://www.sitemaps.org/schemas/sitemap/0.9">

  <xsl:output method="html" encoding="UTF-8" indent="yes"/>

  <xsl:template match="/">
    <html lang="en">
      <head>
        <meta charset="UTF-8"/>
        <title>Sitemap</title>
        <style>
          body {
            margin: 0;
            padding: 40px 20px;
            font-family: Arial, sans-serif;
            background: #f5f7fb;
            color: #1f2937;
          }

          .wrap {
            max-width: 1100px;
            margin: 0 auto;
            background: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.05);
            overflow: hidden;
          }

          .head {
            padding: 28px 32px 18px;
            border-bottom: 1px solid #e5e7eb;
            background: #ffffff;
          }

          h1 {
            margin: 0 0 10px;
            font-size: 28px;
            line-height: 1.2;
            color: #111827;
          }

          p {
            margin: 0;
            color: #6b7280;
            font-size: 15px;
          }

          .meta {
            margin-top: 14px;
            font-size: 14px;
            color: #374151;
          }

          .table-wrap {
            overflow-x: auto;
          }

          table {
            width: 100%;
            border-collapse: collapse;
          }

          th, td {
            padding: 14px 16px;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
            vertical-align: top;
            font-size: 14px;
          }

          th {
            background: #f9fafb;
            color: #111827;
            font-weight: 700;
            position: sticky;
            top: 0;
          }

          tr:hover td {
            background: #f9fbff;
          }

          a {
            color: #2563eb;
            text-decoration: none;
            word-break: break-word;
          }

          a:hover {
            text-decoration: underline;
          }

          .url-text {
            display: block;
            max-width: 100%;
            word-break: break-word;
          }

          .empty {
            padding: 24px 32px;
            color: #6b7280;
          }

          .foot {
            padding: 16px 32px 24px;
            color: #6b7280;
            font-size: 13px;
          }

          @media (max-width: 768px) {
            body {
              padding: 20px 12px;
            }

            .head {
              padding: 22px 18px 16px;
            }

            .foot {
              padding: 14px 18px 20px;
            }

            th, td {
              padding: 12px;
              font-size: 13px;
            }

            h1 {
              font-size: 24px;
            }
          }
        </style>
      </head>
      <body>
        <div class="wrap">
          <div class="head">
            <h1>XML Sitemap</h1>
            <p>Homepage and services pages sitemap.</p>
            <div class="meta">
              Total URLs:
              <strong>
                <xsl:value-of select="count(sitemap:urlset/sitemap:url)"/>
              </strong>
            </div>
          </div>

          <xsl:choose>
            <xsl:when test="count(sitemap:urlset/sitemap:url) &gt; 0">
              <div class="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>URL</th>
                      <th>Last Modified</th>
                      <th>Change Frequency</th>
                      <th>Priority</th>
                    </tr>
                  </thead>
                  <tbody>
                    <xsl:for-each select="sitemap:urlset/sitemap:url">
                      <tr>
                        <td>
                          <a href="{sitemap:loc}" target="_blank" rel="noopener">
                            <span class="url-text">
                              <xsl:value-of select="sitemap:loc"/>
                            </span>
                          </a>
                        </td>
                        <td>
                          <xsl:value-of select="sitemap:lastmod"/>
                        </td>
                        <td>
                          <xsl:value-of select="sitemap:changefreq"/>
                        </td>
                        <td>
                          <xsl:value-of select="sitemap:priority"/>
                        </td>
                      </tr>
                    </xsl:for-each>
                  </tbody>
                </table>
              </div>
            </xsl:when>
            <xsl:otherwise>
              <div class="empty">No URLs found in this sitemap.</div>
            </xsl:otherwise>
          </xsl:choose>

          <div class="foot">
            This view is for humans. Search engines still read the XML sitemap normally.
          </div>
        </div>
      </body>
    </html>
  </xsl:template>
</xsl:stylesheet>
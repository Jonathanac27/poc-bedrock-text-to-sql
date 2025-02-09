DOMAIN_DESCRIPTIONS = {
    "facebook_refined": {
        "schema": "facebook_refined",
        "table": "tb_glue_api_facebook_lead_ads_refined",
        "columns": {
            "campaign_name": "Nome da campanha publicitária no Facebook, usado para identificação e análise.",
            "campaign_id": "Identificador único da campanha publicitária no Facebook.",
            "adset_name": "Nome do conjunto de anúncios dentro da campanha publicitária.",
            "adset_id": "Identificador único do conjunto de anúncios no Facebook.",
            "ad_name": "Nome específico do anúncio dentro do conjunto de anúncios.",
            "ad_id": "Identificador único do anúncio no Facebook.",
            "clicks": "Número total de cliques que o anúncio recebeu.",
            "reach": "Número de pessoas únicas que visualizaram o anúncio.",
            "impressions": "Número total de vezes que o anúncio foi exibido.",
            "objective": "Objetivo principal da campanha publicitária, como leads, cliques no link, etc.",
            "spend": "Valor total gasto na campanha publicitária em uma data específica.",
            "date_start": "Data de início da campanha ou do conjunto de anúncios.",
            "date_stop": "Data de término da campanha ou do conjunto de anúncios.",
            "account_id": "Identificador único da conta de publicidade no Facebook.",
            "inline_link_clicks": "Número de cliques em links dentro do anúncio.",
            "conversions": "Número de conversões geradas pelo anúncio.",
            "inserted_at": "Data e hora em que os dados foram inseridos na esteira de dados, identificador de atualização dos dados.",
            "table_origin": "Origem dos dados, referindo-se à tabela de onde os dados foram extraídos.",
            "timestamp": "Data e hora em que os dados foram coletados."
        }
    },
    "google_refined": {
        "schema": "google_refined",
        "table": "tb_glue_api_google_lead_ads_refined",
        "columns": {
            "integration_id": "ID único da integração para identificar campanhas específicas no sistema.",
            "campaign_id": "ID da campanha publicitária no Google Ads.",
            "campaign_name": "Nome da campanha publicitária no Google Ads.",
            "campaign_advertising_channel_type": "Tipo de canal de publicidade usado na campanha (por exemplo, Pesquisa, Display).",
            "campaign_advertising_channel_sub_type": "Subtipo de canal de publicidade usado na campanha (por exemplo, Vídeos - Pesquisa).",
            "date": "Data em que os dados foram coletados ou reportados.",
            "impressions": "Número de impressões (vezes que o anúncio foi exibido) durante a campanha.",
            "cost": "Custo total da campanha publicitária.",
            "clicks": "Número de cliques recebidos pelo anúncio durante a campanha.",
            "conversions": "Número de conversões resultantes da campanha.",
            "conversions_value": "Valor total das conversões resultantes da campanha.",
            "all_conversions": "Número total de todas as conversões atribuídas à campanha, incluindo aquelas que não são reportadas diretamente.",
            "all_conversions_value": "Valor total de todas as conversões atribuídas à campanha.",
            "status": "Status atual da campanha (por exemplo, ativa, pausada, encerrada).",
            "ad_group_id": "ID do grupo de anúncios dentro da campanha.",
            "ad_group_name": "Nome do grupo de anúncios dentro da campanha.",
            "ad_name": "Nome do anúncio específico dentro do grupo de anúncios.",
            "ad_id": "ID do anúncio específico dentro do grupo de anúncios.",
            "timestamp": "Timestamp de quando os dados foram coletados.",
            "inserted_at": "Data e hora em que os dados foram inseridos na esteira de dados, identificador de atualização dos dados.",
            "table_origin": "Origem dos dados, indicando de qual API ou sistema os dados foram extraídos."
        }
    },
    "linkedin_ads_campaigns": {
        "schema": "linkedin_refined",
        "table": "tb_glue_api_linkedin_lead_ads_campaigns_refined",
        "columns": {
            "id": "Identificador único do anúncio.",
            "name": "Nome ou título do anúncio.",
            "type": "Tipo de anúncio (e.g., SPONSORED_UPDATES, SPONSORED_INMAILS).",
            "optimization_target_type": "Tipo de otimização do anúncio (e.g., MAX_LEAD, MAX_IMPRESSION).",
            "cost_type": "Modelo de custo do anúncio (e.g., CPM).",
            "creative_selection": "Método de seleção criativa (e.g., OPTIMIZED, ROUND_ROBIN).",
            "offsite_delivery_enabled": "Indica se a entrega fora do site está habilitada (true ou false).",
            "audience_expansion_enabled": "Indica se a expansão de audiência está habilitada (true ou false).",
            "format": "Formato do anúncio (e.g., STANDARD_UPDATE, CAROUSEL).",
            "serving_statuses": "Status de exibição do anúncio (e.g., [STOPPED, CAMPAIGN_GROUP_STATUS_HOLD]).",
            "objective_type": "Tipo de objetivo do anúncio (e.g., LEAD_GENERATION, WEBSITE_VISIT).",
            "daily_budget_currency": "Moeda do orçamento diário (e.g., BRL).",
            "daily_budget_amount": "Quantia do orçamento diário.",
            "unit_cost_currency": "Moeda do custo unitário (e.g., BRL).",
            "unit_cost_amount": "Quantia do custo unitário.",
            "account": "Identificador da conta do anúncio.",
            "campaign_group": "Identificador do grupo de campanha.",
            "status": "Status atual do anúncio (e.g., PAUSED, DRAFT).",
            "timestamp": "Data e hora do registro do anúncio.",
            "inserted_at": "Data e hora em que o registro foi inserido no banco de dados.",
            "table_origin": "Origem da tabela de onde os dados foram extraídos."
        }
    },
    "investimentos_refined": {
        "schema": "investimentos_refined",
        "table": "dataset_final",
        "columns": {
            "id_projeto": "Identificador único do projeto.",
            "franqueado": "Nome do franqueado responsável pelo projeto.",
            "cnpj": "CNPJ do franqueado ou empresa associada.",
            "franqueado_id": "Identificador único do franqueado.",
            "vlr_deal": "Valor do contrato do negócio.",
            "origem": "Origem da oportunidade (ex: Inbound, Outbound).",
            "dt_inicio": "Data de início do projeto.",
            "dt_fim": "Data de término do projeto.",
            "lt": "Lead time do projeto (tempo de execução).",
            "id_cliente": "Identificador único do cliente.",
            "ltv_deal": "Valor do ciclo de vida do cliente (LTV).",
            "principal_secao": "Seção principal da empresa dentro do CNAE.",
            "descricao_atividade": "Descrição da atividade principal do franqueado ou empresa.",
            "porte": "Tamanho da empresa (ex: Pequeno, Médio, Grande).",
            "data_inicio": "Data de início das operações da empresa.",
            "id_opp_sales_force": "Identificador da oportunidade no sistema de CRM (Salesforce).",
            "group_segment_desc": "Descrição do grupo de segmento da empresa.",
            "segment_desc": "Descrição detalhada do segmento da empresa.",
            "cnae_session": "Seção CNAE associada à empresa.",
            "cnae_division": "Divisão CNAE da empresa.",
            "cnae_group": "Grupo CNAE da empresa.",
            "cnae_class": "Classe CNAE da empresa.",
            "cnae_sub_class": "Subclasse CNAE da empresa.",
            "churn": "Indicador de churn (cancelamento) do cliente.",
            "investimento_roi_day": "Investimento diário relacionado ao retorno sobre o investimento (ROI).",
            "receita_roi_day": "Receita diária relacionada ao ROI.",
            "margem_roi_day": "Margem diária do ROI.",
            "roi_mean": "Média do ROI ao longo do tempo.",
            "roas_mean": "Média do ROAS (Return on Ad Spend).",
            "roi_latest": "Último valor registrado do ROI.",
            "roi_first": "Primeiro valor registrado do ROI.",
            "roas_latest": "Último valor registrado do ROAS.",
            "roas_first": "Primeiro valor registrado do ROAS.",
            "investimento_latest": "Último valor registrado de investimento.",
            "investimento_first": "Primeiro valor registrado de investimento.",
            "investimento_mean": "Média dos investimentos ao longo do tempo.",
            "receita_latest": "Último valor registrado de receita.",
            "receita_first": "Primeiro valor registrado de receita.",
            "num_registros": "Número total de registros associados ao cliente ou projeto.",
            "vlr_roi_total": "Valor total do ROI acumulado.",
            "vlr_roas_total": "Valor total do ROAS acumulado.",
            "delta_roi": "Variação percentual do ROI.",
            "delta_roas": "Variação percentual do ROAS.",
            "delta_investimento_pct": "Variação percentual no investimento.",
            "delta_receita_pct": "Variação percentual na receita.",
            "vlr_upsell": "Valor de upsell registrado.",
            "vlr_downsell": "Valor de downsell registrado.",
            "down_ltv": "Impacto de downsell no LTV.",
            "up_ltv": "Impacto de upsell no LTV.",
            "vlr_up_down": "Valor total de upsell e downsell.",
            "up_down_ltv": "Impacto combinado de upsell e downsell no LTV.",
            "id_card": "Identificador de referência para o cartão associado ao projeto ou cliente.",
            "num_registros_upsell": "Número de registros associados a upsells.",
            "num_registros_downsell": "Número de registros associados a downsells.",
            "vlr_up_down_category": "Categoria atribuída com base no valor total de upsell e downsell.",
            "ltv_total": "Valor total do ciclo de vida do cliente.",
            "nps_mean": "Média das pontuações do Net Promoter Score (NPS).",
            "nps_most_recent": "Valor mais recente registrado do NPS.",
            "tendencia_nps": "Tendência de variação do NPS ao longo do tempo.",
            "mhs_most_recent": "Valor mais recente do MHS (Medida de Satisfação).",
            "mhs_nota_most_recent": "Última nota registrada do MHS.",
            "mhs_nota_mean": "Média das notas do MHS.",
            "tendencia_mhs": "Tendência de variação do MHS.",
            "n_registros_mhs": "Número de registros associados ao MHS.",
            "mhs_category": "Categoria de satisfação baseada no MHS.",
            "nps_category": "Categoria de satisfação baseada no NPS.",
            "tempo_operacao_anos": "Tempo total de operação da empresa em anos.",
            "categoria_tempo_operacao": "Categoria atribuída com base no tempo de operação.",
            "roi_category": "Categoria atribuída com base no ROI.",
            "roas_category": "Categoria atribuída com base no ROAS.",
            "investimento_category": "Categoria atribuída com base no investimento."
        }
    }
}




